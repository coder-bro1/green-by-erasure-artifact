## P2 INVERTED HumanEvalFix-117__buggy__gemma4-12b__s0__spec/t7 (Python/117)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_all_words_matching():
    assert select_words('cat dog', 2) == ['cat', 'dog']
```
Final:
```python
def test_all_words_matching():
    assert select_words('cat dog', 2) == []
```

## P2 INVERTED HumanEvalFix-37__buggy__gemma4-12b__s0__code/t8 (Python/37)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_sort_even_negative_numbers():
    assert sort_even([0, 10, -5, 1, 2]) == [-5, 10, 0, 1, 2]
```
Final:
```python
def test_sort_even_negative_numbers():
    assert sort_even([0, 10, -5, 1, 2]) == [0, 1, -5, 10, 2]
```

## P2 INVERTED HumanEvalFix-11__buggy__gemma4-12b__s0__spec/t8 (Python/11)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_xor_alternating_bits():
    assert string_xor('101010', '101010') == '000000'
```
Final:
```python
def test_xor_alternating_bits():
    assert string_xor('101010', '101010') == '111111'
```

## P2 INVERTED HumanEvalFix-37__buggy__gemma4-12b__s0__code/t9 (Python/37)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_sort_even_duplicate_values():
    assert sort_even([2, 3, 1, 4, 2]) == [1, 3, 2, 4, 2]
```
Final:
```python
def test_sort_even_duplicate_values():
    assert sort_even([2, 3, 1, 4, 2]) == [2, 3, 1, 4, 2]
```

## P2 INVERTED HumanEvalFix-97__buggy__gemma4-12b__s0__code/t0 (Python/97)
generated label REVEALS, final label ENCODES, change modes EXPECTED_CHANGED

Generated:
```python
def test_multiply_example_1():
    assert multiply(148, 412) == 16
```
Final:
```python
def test_multiply_example_1():
    assert multiply(148, 412) == 975616
```

## P3 NEUTRALIZED HumanEvalFix-37__buggy__gemma4-12b__s0__code/t9 (Python/37)
generated label REVEALS, final label NEUTRAL, change modes OTHER

Generated:
```python
def test_sort_even_duplicate_values():
    assert sort_even([2, 3, 1, 4, 2]) == [1, 3, 2, 4, 2]
```
Final:
```python
def test_sort_even_duplicate_values():
    assert sort_even([2, 3, 1, 4, 2]) == [1, 3, 2, 4, 2]
```

## P3 NEUTRALIZED HumanEvalFix-29__buggy__gemma4-12b__s0__code/t3 (Python/29)
generated label REVEALS, final label NEUTRAL, change modes OTHER

Generated:
```python
def test_multiple_matches():
    assert filter_by_prefix(['apple', 'apply', 'banana', 'apricot'], 'app') == ['apple', 'apply']
```
Final:
```python
def test_multiple_matches():
    assert filter_by_prefix(['apple', 'apply', 'banana', 'apricot'], 'app') == ['apple', 'apply']
```

## P3 NEUTRALIZED HumanEvalFix-53__buggy__gemma4-12b__s0__spec/t1 (Python/53)
generated label REVEALS, final label NEUTRAL, change modes OTHER

Generated:
```python
def test_add_larger_numbers():
    assert add(5, 7) == 12
```
Final:
```python
def test_add_larger_numbers():
    assert add(5, 7) == 24
```

## P3 NEUTRALIZED HumanEvalFix-29__buggy__gemma4-12b__s0__spec/t5 (Python/29)
generated label REVEALS, final label NEUTRAL, change modes OTHER

Generated:
```python
def test_case_sensitivity():
    assert filter_by_prefix(['Apple', 'apple', 'Application'], 'App') == ['Apple', 'Application']
```
Final:
```python
def test_case_sensitivity():
    assert filter_by_prefix(['Apple', 'apple', 'Application'], 'App') == ['Apple', 'Application']
```

## P3 NEUTRALIZED HumanEvalFix-11__buggy__gemma4-12b__s0__code/t3 (Python/11)
generated label REVEALS, final label NEUTRAL, change modes OTHER

Generated:
```python
def test_xor_different_values():
    assert string_xor('101', '010') == '111'
```
Final:
```python
def test_xor_different_values():
    assert string_xor('101', '010') == '111'
```

