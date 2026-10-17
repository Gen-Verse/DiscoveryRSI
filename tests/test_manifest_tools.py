from discovery_rsi.manifest import ResearchManifest
from discovery_rsi.tools import default_registry

def test_manifest_and_tools_are_portable():
    m = ResearchManifest.from_dict({"name":"x","question":"q","domains":["geo_pathway"]})
    assert m.domains == ("geo_pathway",)
    registry = default_registry()
    assert "falsify" in registry.names()
    assert registry.call("falsify", criterion="null") == {"falsification":"null"}
