from emport import import_file

def test_importing_doesnt_emit_warnings(tmpdir, module_file_factory, recwarn):
    import warnings
    warnings.simplefilter('always')
    filename, _ = module_file_factory(tmpdir)
    module = import_file(filename)
    assert len(recwarn.list) == 0
