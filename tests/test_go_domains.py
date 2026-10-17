from discovery_rsi.go_domains import GOPathwayAdapter, GOTargetPrioritizationAdapter

def test_go_pathway_adapter_is_deterministic_and_filters_short_sets():
    adapter = GOPathwayAdapter.from_records([
        {"term_id": "GO:0001", "name": "Signal relay", "genes": ["B", "A"]},
        {"term_id": "GO:0002", "name": "Too small", "genes": ["A"]},
    ])
    out = adapter.candidates(episode=2)
    assert len(out) == 1
    assert out[0].id == "go-pathway-2-1"
    assert "GO:0001" in out[0].claim
    assert "null permutation" in out[0].plan

def test_go_target_prioritization_makes_alternatives_explicit():
    adapter = GOTargetPrioritizationAdapter.from_records([
        {"target": "GENE1", "term_ids": ["GO:0001"], "evidence": ["expression"]}
    ], prioritized_terms=["GO:0001"])
    out = adapter.candidates()
    assert len(out) == 1
    assert "GENE1" in out[0].claim
    assert "well-studied" in out[0].alternatives[0]
    assert "expression" in out[0].evidence
