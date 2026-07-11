def test_integration_fixtures_load(
    coach_html,
    inspection,
    repository,
    parser,
    normalizer,
    verifier,
    client,
    synchronization_service,
):
    assert coach_html
    assert inspection is not None
    assert repository is not None
    assert parser is not None
    assert normalizer is not None
    assert verifier is not None
    assert client is not None
    assert synchronization_service is not None
