def test_save__new_supplement__ok(supplement_repository, supplement_factory):
    supplement = supplement_factory()
    supplement_repository.save(supplement)

    saved_supplement = supplement_repository.supplement_of_id(supplement.id(), supplement.tenant_id())

    assert saved_supplement == supplement


def test_save__existing_supplement__no_error(supplement_repository, supplement_factory):
    supplement = supplement_factory()
    supplement_repository.save(supplement)
    supplement_repository.save(supplement)


def test_save__changed_supplement_data__ok(supplement_repository, supplement_factory, extra_data_factory):
    supplement = supplement_factory()
    supplement_repository.save(supplement)

    supplement.data = [extra_data_factory(), extra_data_factory(), extra_data_factory()]
    supplement_repository.save(supplement)

    changed_supplement = supplement_repository.supplement_of_id(supplement.id(), supplement.tenant_id())

    assert changed_supplement.data == supplement.data


def test_delete__existing_supplement__ok(supplement_repository, supplement_factory):
    supplement = supplement_factory()
    supplement_repository.save(supplement)
    supplement_repository.delete(supplement)

    deleted_supplement = supplement_repository.supplement_of_id(supplement.id(), supplement.tenant_id())

    assert deleted_supplement is None


def test_delete__non_existing_supplement__no_error(supplement_repository, supplement_factory):
    supplement = supplement_factory()

    supplement_repository.delete(supplement)


def test_get__non_existing_supplement__none_returned(supplement_repository):
    supplement = supplement_repository.supplement_of_id("test_id", "test_tenant_id")

    assert supplement is None
