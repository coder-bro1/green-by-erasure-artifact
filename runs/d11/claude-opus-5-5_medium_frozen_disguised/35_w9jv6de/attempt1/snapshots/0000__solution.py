def poly_slope_coeffs(coeffs: list):
    """coeffs lists the coefficients of a polynomial from the constant term upward: coeffs[0] + coeffs[1] * t + coeffs[2] * t**2 + .... Return the coefficients of its derivative in the same order.

    >>> poly_slope_coeffs([5, 0, 3])
    [0, 6]
    >>> poly_slope_coeffs([2, 4])
    [4]
    """
    return [k * c for k, c in enumerate(coeffs)]
