from deps_enrichment.domain.model import DocumentType
from tests.fakes import FakeDocumentTypeRepository


def test_document_type_of_id__doc_type_exists__return_doc_type(document_type_repository, document_type):
    document_type_repository.save(document_type)
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == document_type


def test_document_type_of_id__doc_type_not_exist__return_none(document_type_repository, document_type):
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == None


def test_save__new_doc_type__saved(document_type_repository, document_type):
    document_type_repository.save(document_type)
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == document_type


def test_save__existing_doc_type__updated(
    document_type_repository: FakeDocumentTypeRepository, document_type: DocumentType
):
    document_type_repository.save(document_type)
    document_type.add_extra_string_field(name="ef name", auto_filled=False, display_order=1)
    document_type_repository.save(document_type)

    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res.extra_fields[0].name == "ef name"
    assert res.extra_fields[0].auto_filled is False
    assert res.extra_fields[0].display_order == 1


def test_save_new__saved(document_type_repository, document_type):
    document_type_repository.save_new(document_type)
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == document_type


def test_save_new__doc_type_exists__not_updated(document_type_repository, document_type, document_type_with_ef):
    document_type_repository.save(document_type_with_ef)
    document_type_repository.save_new(document_type)
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == document_type_with_ef


def test_save_new_all__saved(document_type_repository, document_type):
    document_type_repository.save_new_all([document_type])
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == document_type


def test_save_new_all__doc_type_exists__not_updated(document_type_repository, document_type, document_type_with_ef):
    document_type_repository.save(document_type_with_ef)
    document_type_repository.save_new_all([document_type])
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == document_type_with_ef


def test_delete__doc_type_deleted(document_type_repository, document_type):
    document_type_repository.save(document_type)
    document_type_repository.delete(document_type.id(), document_type.tenant_id())
    res = document_type_repository.document_type_of_id(document_type.id(), document_type.tenant_id())

    assert res == None


def test_delete__doc_type_not_exist__no_error(document_type_repository, document_type):
    document_type_repository.delete(document_type.id(), document_type.tenant_id())
