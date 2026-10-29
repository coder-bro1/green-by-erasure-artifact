## P2 INVERTED HumanEvalPlusNatural-97__buggy__gemma4-12b__s0__code/t9 (HumanEvalPlusNatural/97)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_multiply_mixed_signs():
    assert multiply(55, -66) == 30
```
Final:
```python
def test_multiply_mixed_signs():
    assert multiply(55, -66) == 20
```

## P2 INVERTED HumanEvalPlusNatural-10__buggy__gemma4-12b__s0__code/t8 (HumanEvalPlusNatural/10)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_complex_palindrome_suffix():
    assert make_palindrome('banana') == 'bananab'
```
Final:
```python
def test_complex_palindrome_suffix():
    assert make_palindrome('banana') == 'bananananab'
```

## P2 INVERTED HumanEvalPlusNatural-32__buggy__gemma4-12b__s0__code/t6 (HumanEvalPlusNatural/32)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_quadratic_perfect_square():
    result = find_zero([25, -10, 1])
    assert round(result, 2) == 5.0
```
Final:
```python
def test_quadratic_perfect_square():
    result = find_zero([25, -10, 1])
    assert round(result, 2) == 1000000.0
```

## P2 INVERTED HumanEvalPlusNatural-10__buggy__gemma4-12b__s0__code/t7 (HumanEvalPlusNatural/10)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_palindrome_suffix_three_chars():
    assert make_palindrome('abcc') == 'abccba'
```
Final:
```python
def test_palindrome_suffix_three_chars():
    assert make_palindrome('abcc') == 'abcccba'
```

## P2 INVERTED HumanEvalPlusNatural-10__buggy__gemma4-12b__s0__code/t6 (HumanEvalPlusNatural/10)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_palindrome_suffix_two_chars():
    assert make_palindrome('abb') == 'abba'
```
Final:
```python
def test_palindrome_suffix_two_chars():
    assert make_palindrome('abb') == 'abbba'
```

## P3 NEUTRALIZED HumanEvalPlusNatural-10__buggy__gemma4-12b__s0__code/t7 (HumanEvalPlusNatural/10)
generated label REVEALS, final label NEUTRAL, change modes FUNCTION_SHADOWED

Generated:
```python
def test_palindrome_suffix_three_chars():
    assert make_palindrome('abcc') == 'abccba'
```
Final:
```python
def test_palindrome_suffix_three_chars():
    assert make_palindrome('abcc') == 'abcccba'
```

## P3 NEUTRALIZED HumanEvalPlusNatural-32__buggy__gemma4-12b__s0__code/t9 (HumanEvalPlusNatural/32)
generated label REVEALS, final label NEUTRAL, change modes FUNCTION_SHADOWED

Generated:
```python
def test_far_root_expansion():
    assert round(find_zero([1, 1e-06]), 2) == -1000000.0
```
Final:
```python
def test_far_root_expansion():
    assert round(find_zero([1, 1e-06]), 2) == 1000000.0
```

## P3 NEUTRALIZED HumanEvalPlusNatural-10__buggy__gemma4-12b__s0__code/t8 (HumanEvalPlusNatural/10)
generated label REVEALS, final label NEUTRAL, change modes FUNCTION_SHADOWED

Generated:
```python
def test_complex_palindrome_suffix():
    assert make_palindrome('banana') == 'bananab'
```
Final:
```python
def test_complex_palindrome_suffix():
    assert make_palindrome('banana') == 'bananab'
```

## P3 NEUTRALIZED HumanEvalPlusNatural-10__buggy__gemma4-12b__s0__code/t10 (HumanEvalPlusNatural/10)
generated label REVEALS, final label NEUTRAL, change modes FUNCTION_SHADOWED

Generated:
```python
def test_overlapping_palindrome_logic():
    assert make_palindrome('cata') == 'catac'
```
Final:
```python
def test_overlapping_palindrome_logic():
    assert make_palindrome('cata') == 'catac'
```

