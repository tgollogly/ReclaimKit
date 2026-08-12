"""ReclaimKit test suite."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.campaign import init_campaign, load_state, record_refusal, record_sent, save_state
from src.config import ConfigError, load_config, validate_config
from src.doctor import run_doctor
from src.escalation_letters import GOOGLE_ROUNDS, META_ROUNDS, TRACKS
from src.security import allowed_recipient, clamp_text, resolve_under, sanitize_filename

EXAMPLE_CONFIG_PATH = Path("config.example.yaml")


SAMPLE_CONFIG = {
    "subject": {
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "+44 1234",
        "address_line1": "1 Test St",
        "city": "Newry",
        "postcode": "BT35 6XX",
        "country": "United Kingdom",
    },
    "case": {
        "facebook": {
            "group_name": "Test Group",
            "post_date": "2025-06-05",
            "post_caption": "test caption",
            "post_url": "https://www.facebook.com/groups/1/posts/2/",
        },
        "alleged_commenters": [],
    },
    "evidence": {
        "screenshots_dir": "./evidence/screenshots",
        "output_dir": "./output",
    },
    "monitor": {"search_queries": ['"Test User"'], "region": "uk-en"},
}


@pytest.fixture
def tmp_config(tmp_path: Path):
    cfg = dict(SAMPLE_CONFIG)
    cfg["evidence"] = {
        "screenshots_dir": str(tmp_path / "screenshots"),
        "output_dir": str(tmp_path / "output"),
    }
    (tmp_path / "screenshots").mkdir()
    (tmp_path / "output").mkdir()
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
subject:
  full_name: Test User
  email: test@example.com
  phone: "+44 1234"
  address_line1: "1 Test St"
  city: Newry
  postcode: BT35 6XX
  country: United Kingdom
case:
  facebook:
    group_name: Test Group
    post_date: "2025-06-05"
    post_caption: test caption
    post_url: https://www.facebook.com/groups/1/posts/2/
  alleged_commenters: []
evidence:
  screenshots_dir: {screenshots}
  output_dir: {output}
monitor:
  search_queries:
    - "\\"Test User\\""
  region: uk-en
""".format(
            screenshots=str(tmp_path / "screenshots"),
            output=str(tmp_path / "output"),
        ),
        encoding="utf-8",
    )
    cfg = load_config(config_path)
    return config_path, cfg


def test_validate_config_ok(tmp_config):
    _, cfg = tmp_config
    validate_config(cfg)


def test_validate_config_missing_email(tmp_config):
    _, cfg = tmp_config
    del cfg["subject"]["email"]
    with pytest.raises(ConfigError):
        validate_config(cfg)


def test_validate_config_bad_url(tmp_config):
    _, cfg = tmp_config
    cfg["case"]["facebook"]["post_url"] = "ftp://bad"
    with pytest.raises(ConfigError):
        validate_config(cfg)


def test_load_config_file(tmp_config):
    path, _ = tmp_config
    loaded = load_config(path)
    assert loaded["subject"]["full_name"] == "Test User"


def test_path_traversal_blocked(tmp_path):
    base = tmp_path / "evidence"
    base.mkdir()
    with pytest.raises(ValueError):
        resolve_under(base, "../../etc/passwd")


def test_sanitize_filename_rejects_dotdot():
    with pytest.raises(ValueError):
        sanitize_filename("../evil.png")


def test_allowed_recipient_meta_only():
    assert allowed_recipient("privacy@facebook.com") == "privacy@facebook.com"
    with pytest.raises(ValueError):
        allowed_recipient("attacker@evil.com")


def test_meta_round1_letter_contains_url(tmp_config):
    _, cfg = tmp_config
    letter = META_ROUNDS[1][1](cfg, {})
    assert "Article 17" in letter
    assert cfg["case"]["facebook"]["post_url"] in letter
    assert "Community Standards" in letter
    assert "privacy@facebook.com" in letter


def test_meta_round1_cites_reports_when_configured(tmp_config):
    _, cfg = tmp_config
    cfg["case"]["facebook"]["meta_reports"] = [
        {"type": "In-app report", "date": "2026-08-12", "outcome": "Rejected"},
    ]
    letter = META_ROUNDS[1][1](cfg, {})
    assert "Rejected" in letter
    assert "Article 17(3)" in letter or "Article 17" in letter


def test_google_round1_includes_defamation_grounds(tmp_config):
    _, cfg = tmp_config
    from src.escalation_letters import GOOGLE_ROUNDS

    gletter = GOOGLE_ROUNDS[1][1](cfg, {})
    assert "Defamation" in gletter
    assert "serious reputational harm" in gletter.lower()


def test_campaign_state_roundtrip(tmp_config):
    _, cfg = tmp_config
    state = init_campaign(cfg, Path(cfg["evidence"]["output_dir"]))
    record_sent(state, "meta", 1)
    path = save_state(state, Path(cfg["evidence"]["output_dir"]) / "campaign" / "state.json")
    loaded = load_state(path)
    assert loaded["tracks"]["meta"]["round"] == 1


def test_record_refusal_requires_reason(tmp_config):
    _, cfg = tmp_config
    state = init_campaign(cfg, Path(cfg["evidence"]["output_dir"]))
    record_sent(state, "meta", 1)
    with pytest.raises(ValueError):
        record_refusal(state, "meta", "   ")


def test_clamp_text():
    assert len(clamp_text("x" * 100, 10)) == 10


def test_doctor_runs(tmp_config):
    path, _ = tmp_config
    report = run_doctor(str(path))
    assert "checks" in report
    assert isinstance(report["checks"], list)


def test_config_example_validates():
    cfg = yaml.safe_load(EXAMPLE_CONFIG_PATH.read_text(encoding="utf-8"))
    validate_config(cfg)
    assert cfg["case"]["facebook"].get("meta_reports")


def test_all_letter_rounds_from_example_config():
    cfg = yaml.safe_load(EXAMPLE_CONFIG_PATH.read_text(encoding="utf-8"))
    for track, rounds in TRACKS.items():
        for round_num, (_, fn, _, _) in rounds.items():
            text = fn(cfg, {})
            assert len(text) > 200, f"{track} r{round_num} too short"
            if track == "meta":
                assert "Article 17" in text or "GDPR" in text
            elif track == "google":
                assert "Google" in text or "Defamation" in text
            else:
                assert "ICO" in text or "Article 17" in text


def test_uncertain_post_origin_wording(tmp_config):
    _, cfg = tmp_config
    cfg["case"]["facebook"]["post_origin"] = "uncertain"
    letter = META_ROUNDS[1][1](cfg, {})
    assert "without prejudice" in letter
    assert "published without my knowledge or consent" not in letter


def test_third_party_post_origin_wording(tmp_config):
    _, cfg = tmp_config
    cfg["case"]["facebook"]["post_origin"] = "third_party"
    letter = META_ROUNDS[1][1](cfg, {})
    assert "did not create" in letter or "did not authorise" in letter


def test_config_example_has_post_origin_uncertain():
    cfg = yaml.safe_load(EXAMPLE_CONFIG_PATH.read_text(encoding="utf-8"))
    assert cfg["case"]["facebook"].get("post_origin") == "uncertain"


def test_search_queries_url_encoded():
    cfg = yaml.safe_load(EXAMPLE_CONFIG_PATH.read_text(encoding="utf-8"))
    text = GOOGLE_ROUNDS[1][1](cfg, {})
    assert "search?q=" in text
    assert "%22Thomas" in text or "Thomas+Gollogly" in text
