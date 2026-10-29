# C1 section 10: developers' tests lifted into the harness

Computed by `analysis/c1_devtests.py`. Kept: fails on buggy and passes on fixed, twice each.

| Bug | Test | Result | Buggy | Fixed |
|---|---|---|---|---|
| cookiecutter-1 | test_generate_context_decodes_non_ascii_chars | not kept | PUT_EXCEPTION, PUT_EXCEPTION | PUT_EXCEPTION, PUT_EXCEPTION |
| cookiecutter-3 | test_click_invocation | not kept | TEST_ERROR, TEST_ERROR | TEST_ERROR, TEST_ERROR |
| httpie-3 | TestSession::test_download_in_session | not lifted: class has base classes (SessionTestBase) | | |
| httpie-4 | test_Host_header_overwrite | kept | ASSERT_FAIL, ASSERT_FAIL | PASS, PASS |
| luigi-20 | TaskTest::test_task_to_str_to_task | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-21 | InterfaceTest::test_just_run_main_task_cls | not lifted: class has base classes (LuigiTestCase) | | |
| luigi-25 | TestS3CopyToTable::test_s3_copy_to_table | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-28 | HiveCommandClientTest::test_table_exists | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-28 | HiveCommandClientTest::test_apacheclient_table_exists | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-31 | CentralPlannerTest::test_assistant_get_work_external_task | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-33 | ParameterTest::test_local_insignificant_param | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-33 | TestRemoveGlobalParameters::test_global_significant_param | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-33 | TestRemoveGlobalParameters::test_mixed_params | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-33 | TestRemoveGlobalParameters::test_mixed_params_inheritence | not lifted: class has base classes (unittest.TestCase) | | |
| luigi-4 | TestS3CopyToTable::test_s3_copy_with_nonetype_columns | not lifted: class has base classes (unittest.TestCase) | | |
| pandas-119 | TestPivotTable::test_margins_casted_to_float | not lifted: uses fixtures (observed) | | |
| pandas-127 | TestTimeSeries::test_pct_change_with_duplicate_axis | kept | PUT_EXCEPTION, PUT_EXCEPTION | PASS, PASS |
| pandas-161 | TestSeriesMissingData::test_fillna_categorical_with_new_categories | kept | TEST_ERROR, TEST_ERROR | PASS, PASS |
| pandas-162 | TestCrosstab::test_margin_normalize | kept | PUT_EXCEPTION, PUT_EXCEPTION | PASS, PASS |
| pandas-168 | test_groupby_axis_1 | kept | PUT_EXCEPTION, PUT_EXCEPTION | PASS, PASS |
| pandas-23 | TestDatetimeIndexSetOps::test_intersection_empty | not kept | TEST_ERROR, TEST_ERROR | TEST_ERROR, TEST_ERROR |
| pandas-23 | TestBusinessDatetimeIndex::test_intersection_bug | kept | ASSERT_FAIL, ASSERT_FAIL | PASS, PASS |
| pandas-23 | TestCustomDatetimeIndex::test_intersection_bug | kept | ASSERT_FAIL, ASSERT_FAIL | PASS, PASS |
| pandas-58 | TestCategoricalConstructors::test_from_codes_with_nullable_int | kept | PUT_EXCEPTION, PUT_EXCEPTION | PASS, PASS |
| pandas-58 | TestCategoricalConstructors::test_from_codes_with_nullable_int_na_raises | kept | TEST_ERROR, TEST_ERROR | PASS, PASS |
| pandas-69 | TestFloat64Index::test_lookups_datetimelike_values | not lifted: class has base classes (Numeric) | | |
| sanic-1 | test_bp_middleware_order | not lifted: uses fixtures (app) | | |
| sanic-3 | test_routes_with_host | not lifted: uses fixtures (app) | | |
| spacy-2 | test_issue5137 | kept | ASSERT_FAIL, ASSERT_FAIL | PASS, PASS |
| tornado-11 | server_test.HTTPServerRawTest.test_chunked_request_uppercase | not lifted: unittest | | |
| tornado-13 | ction_test.HTTP1ConnectionTest.test_http10_no_content_length | not lifted: unittest | | |
| tornado-14 | ornado.test.ioloop_test.TestIOLoopCurrent.test_force_current | not lifted: unittest | | |
| tornado-2 | test.HTTPClientCommonTestCase.test_redirect_put_without_body | not lifted: unittest | | |
| tornado-3 | tornado.test.httpclient_test.SyncHTTPClientSubprocessTest | not lifted: unittest | | |
| tornado-4 | eb_test.StaticFileTest.test_static_with_range_neg_past_start | not lifted: unittest | | |
| tornado-4 | FileTest.test_static_unsatisfiable_range_end_less_than_start | not lifted: unittest | | |
| tornado-5 | st.ioloop_test.TestPeriodicCallbackMath.test_clock_backwards | not lifted: unittest | | |
| tornado-8 | test.websocket_test.WebSocketTest.test_missing_websocket_key | not lifted: unittest | | |

Kept: 10 tests in 8 bugs.
