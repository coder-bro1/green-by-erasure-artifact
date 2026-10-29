import pytest

from solution import validate_filename


# --- Docstring examples -----------------------------------------------------

def test_docstring_examples():
    assert validate_filename('report7.exe') == 'Yes'
    assert validate_filename('7report.exe') == 'No'
    assert validate_filename('x1234.txt') == 'No'


# --- Valid names --------------------------------------------------------------

@pytest.mark.parametrize('name', [
    'a.txt',
    'Z.exe',
    'file.dll',
    'example.txt',
    'MyFile.exe',
    'a1.txt',
    'a12.dll',
    'a123.exe',      # exactly three digits is allowed
    'a1b2c3.txt',    # three non-adjacent digits
    'a_b-c d.txt',   # other characters after the first letter are fine
])
def test_valid_names(name):
    assert validate_filename(name) == 'Yes'


# --- Dot count ------------------------------------------------------------------

@pytest.mark.parametrize('name', [
    'filetxt',        # no dot
    '',               # empty string
    'file.tar.txt',   # two dots
    'a..txt',         # two adjacent dots
    'file.txt.',      # trailing dot
    '...',
])
def test_requires_exactly_one_dot(name):
    assert validate_filename(name) == 'No'


# --- Part before the dot --------------------------------------------------------

@pytest.mark.parametrize('name', [
    '.txt',       # empty stem
    '1file.txt',  # starts with digit
    '_file.exe',  # starts with underscore
    ' file.dll',  # starts with space
    '-a.txt',     # starts with hyphen
])
def test_stem_must_start_with_letter(name):
    assert validate_filename(name) == 'No'


# --- Digit limit ----------------------------------------------------------------

@pytest.mark.parametrize('name', [
    'a1234.txt',
    'a1b2c3d4.exe',
    'a0000.dll',
])
def test_more_than_three_digits_rejected(name):
    assert validate_filename(name) == 'No'


# --- Return type ----------------------------------------------------------------

@pytest.mark.parametrize('name', ['a.txt', '1.txt', ''])
def test_returns_yes_or_no_string(name):
    assert validate_filename(name) in ('Yes', 'No')


# --- Spec requirements that solution.py does NOT currently satisfy -------------
# These are marked strict xfail: they document real bugs. If solution.py is
# fixed, they will XPASS and the strict marker will flag that the xfail should
# be removed.

@pytest.mark.xfail(strict=True, reason='BUG: extension is never checked against txt/exe/dll')
@pytest.mark.parametrize('name', [
    'file.pdf',
    'file.',        # empty extension
    'file.TXT',     # extensions are case-sensitive per spec
    'file.txtx',
    'file.ex',
    'a.1234',
])
def test_extension_must_be_allowed(name):
    assert validate_filename(name) == 'No'


@pytest.mark.xfail(strict=True, reason='BUG: str.isalpha() accepts non-Latin letters')
@pytest.mark.parametrize('name', [
    'école.txt',     # e-acute
    'файл.exe',  # Cyrillic
    '文件.dll',   # CJK
])
def test_first_char_must_be_latin_letter(name):
    assert validate_filename(name) == 'No'
