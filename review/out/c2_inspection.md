# C2: commit-level inspection of the 13 possible erasures

Read-only GitHub API. For each case: the commits that changed an expected value, their message, and the
test-file hunk around the change.

## C004: swingerman/ha-dual-smart-thermostat#431 (Copilot, merged yes)

Add E2E CI workflow for automated integration testing

Commit 954f489d5b: test: basic heater e2e first working stable flow

File tests/config_flow/test_config_flow.py:

```diff
@@ -64,7 +64,7 @@ async def test_ac_only_config_flow():
     result = await flow.async_step_user(user_input)
 
     assert result["type"] == "form"
-    assert result["step_id"] == "cooling_only"
+    assert result["step_id"] == "basic_ac"
 
     # Step 2: Cooling configuration
     cooling_input = {
@@ -78,7 +78,7 @@ async def test_ac_only_config_flow():
             CONF_KEEP_ALIVE: 300,
         },
     }
-    result = await flow.async_step_cooling_only(cooling_input)
```

Commit 857a37abb6: fix: update AC-only config flow test step IDs and method calls

File tests/config_flow/test_config_flow.py:

```diff
@@ -64,7 +64,7 @@ async def test_ac_only_config_flow():
     result = await flow.async_step_user(user_input)
 
     assert result["type"] == "form"
-    assert result["step_id"] == "basic_ac"
+    assert result["step_id"] == "basic_ac_only"
 
     # Step 2: Cooling configuration
     cooling_input = {
@@ -78,7 +78,7 @@ async def test_ac_only_config_flow():
             CONF_KEEP_ALIVE: 300,
         },
     }
-    result = await flow.async_step_basic_ac(cooling_input)
```

## C007: NewFuture/DDNS#539 (Copilot, merged yes)

feat(config): 支持远程配置文件 add remote HTTP(S) config loading support

Commit 64b8055008: feat(http): add default User-Agent handling in request function and enhance related tests

File tests/test_util_http.py:

```diff
@@ -47,172 +48,100 @@ def byte_string(s):
 class TestUserAgent(unittest.TestCase):
     """测试 USER_AGENT 常量和用户代理头部设置"""
 
-    def test_user_agent_constant(self):
-        """测试USER_AGENT常量格式正确"""
-        # 验证USER_AGENT常量存在且格式正确
-        self.assertIsInstance(USER_AGENT, text_type)
-        self.assertIn("DDNS/", USER_AGENT)
-        self.assertIn("<email>", USER_AGENT)
-
-    def test_user_agent_version_format(self):
-        """测试USER_AGENT包含版本信息"""
-        # USER_AGENT应该包含版本号或"dev"
-        has_version = any(char.isdigit() for char in USER_AGENT) or "dev" in USER_AGENT
-        self.assertTrue(has_version, "USER_AGENT should contain version number or 'dev'")
-
-    def test_request_sets_user_agent_automatically(self):
-        """测试request函数自动设置User-Agent头部"""
+    def _test_user_agent_with_endpoints(self, headers=None, expected_ua=None):
+        """通用的User-Agent测试辅助方法"""
         from ddns.util.http import request
 
-        # 多个测试站点，按可靠性排序
+        # 多个测试站点，随机顺序以分散负载
         test_endpoints = [
-            "http://pie.dev/headers",
+            "https://httpbingo.org/user-agent",
             "http://postman-echo.com/headers",
             "http://httpbin.org/user-agent",
         ]
+        if not expected_ua:
+            test_endpoints.remove("https://httpbingo.org/user-agent")  # 如果不验证User-Agent，则不需要这个端点
+        random.shuffle(test_endpoints)
 
         for endpoint in test_endpoints:
             try:
-                response = request("GET", endpoint, retries=1)
-
+                response = request("GET", endpoint, headers=headers, retries=1)
                 if response.status == 200:
                     response_data = json.loads(response.body)
-
                     # 不同的测试站点响应格式可能略有不同
-                    if "headers" in response_data:
-                        headers = response_data["headers"]
-                        user_agent_key = None
-                        # 查找User-Agent头部（不区分大小写）
-                        for key in headers:
-                            if key.lower() == "user-agent":
-                                user_agent_key = key
-                                break
-
-                        if user_agent_key:
-                            self.assertEqual(headers[user_agent_key], USER_AGENT)
-                            return  # 测试成功，退出
-                    elif "user-agent" in response_data:
-                        # httpbin.org/user-agent 的格式
-                        self.assertEqual(response_data["user-agent"], USER_AGENT)
-                        return  # 测试成功，退出
-
-            except Exception as e:
-                # 记录当前端点失败，继续尝试下一个
+                    headers = response_data["headers"] if "headers" in response_data else response_data
+                    # 查找User-Agent头部（不区分大小写）
+                    ua_key = next((key for key in headers if key.lower() == "user-agent"), None)
+                    if ua_key:
+                        ua_value = headers[ua_key]
+                        if expected_ua:
+                            self.assertEqual(ua_value, expected_ua)
+                        else:
+                            # 只验证不是None和空字符串
+                            self.assertIn(ua_value, (None, ""))
+                    else:
+                        self.assertIn(ua_value, (None, ""))
+                    return True  # 测试成功
+
+            except OSError as e:
                 error_msg = str(e).lower()
+                # 不允许None错误时，网络问题继续尝试，其他错误重新抛出
                 network_keywords = ["timeout", "connection", "resolution", "unreachable", "network"]
                 if not any(keyword in error_msg for keyword in network_keywords):
                     # 如果不是网络问题，重新抛出异常
                     raise
                 continue
 
         # 所有端点都失败
-        self.skipTest("All test endpoints unavailable for user-agent test")
+        return False
+
+    def test_user_agent_constant(self):
+        """测试USER_AGENT常量格式正确"""
+        # 验证USER_AGENT常量存在且格式正确
+        self.assertIsInstance(USER_AGENT, text_type)
+        self.assertIn("DDNS/", USER_AGENT)
+        self.assertIn("<email>", USER_AGENT)
+
+    def test_user_agent_version_format(self):
+        """测试USER_AGENT包含版本信息"""
+        # USER_AGENT应该包含版本号或"dev"
+        has_version = any(char.isdigit() for char in USER_AGENT) or "dev" in USER_AGENT
+        self.assertTrue(has_version, "USER_AGENT should contain version number or 'dev'")
+
+    def test_request_sets_user_agent_automatically(self):
+        """测试request函数自动设置User-Agent头部"""
+        if not self._test_user_agent_with_endpoints(expected_ua=USER_AGENT):
+            self.skipTest("All test endpoints unavailable for user-agent test")
 
     def test_custom_user_agent_override(self):
         """测试自定义User-Agent头部会覆盖默认值"""
-        from ddns.util.http import request
-
         custom_ua = "CustomAgent/1.0"
         headers = {"User-Agent": custom_ua}
 
-        # 多个测试站点，按可靠性排序
-        test_endpoints = [
-            "http://pie.dev/headers",
-            "http://postman-echo.com/headers",
-            "http://httpbin.org/user-agent",
-        ]
-
-        for endpoint in test_endpoints:
-            try:
-                response = request("GET", endpoint, headers=headers, retries=1)
-
-                if response.status == 200:
-                    response_data = json.loads(response.body)
-
-                    # 不同的测试站点响应格式可能略有不同
-                    if "headers" in response_data:
-                        response_headers = response_data["headers"]
-                        user_agent_key = None
-                        # 查找User-Agent头部（不区分大小写）
-                        for key in response_headers:
-                            if key.lower() == "user-agent":
-                                user_agent_key = key
-                                break
-
-                        if user_agent_key:
-                            self.assertEqual(response_headers[user_agent_key], custom_ua)
-                            self.assertNotEqual(response_headers[user_agent_key], USER_AGENT)
-                            return  # 测试成功，退出
-                    elif "user-agent" in response_data:
-                        # httpbin.org/user-agent 的格式
-                        self.assertEqual(response_data["user-agent"], custom_ua)
-                        self.assertNotEqual(response_data["user-agent"], USER_AGENT)
-                        return  # 测试成功，退出
-
-            except Exception as e:
-                # 记录当前端点失败，继续尝试下一个
-                error_msg = str(e).lower()
-                network_keywords = ["timeout", "connection", "resolution", "unreachable", "network"]
-                if not any(keyword in error_msg for keyword in network_keywords):
-                    # 如果不是网络问题，重新抛出异常
-                    raise
-                continue
-
-        # 所有端点都失败
-        self.skipTest("All test endpoints unavailable for custom user-agent test")
+        if self._test_user_agent_with_endpoints(headers=headers, expected_ua=custom_ua):
+            # 额外验证不是默认的USER_AGENT
+            self.assertNotEqual(custom_ua, USER_AGENT)
+        else:
+            self.skipTest("All test endpoints unavailable for custom user-agent test")
 
     def test_case_insensitive_user_agent_header(self):
         """测试User-Agent头部大小写不敏感处理"""
-        from ddns.util.http import request
-
         custom_ua = "TestAgent/2.0"
         # 使用小写的user-agent头部
         headers = {"user-agent": custom_ua}
 
-        # 多个测试站点，按可靠性排序
-        test_endpoints = [
-            "http://postman-echo.com/headers" "http://pie.dev/headers",
-            "http://httpbin.org/user-agent",
-        ]
+        if self._test_user_agent_with_endpoints(headers=headers, expected_ua=custom_ua):
+            # 额外验证不是默认的USER_AGENT
+            self.assertNotEqual(custom_ua, USER_AGENT)
+        else:
+            self.skipTest("All test endpoints unavailable for case-insensitive user-agent test")
 
-        for endpoint in test_endpoints:
-            try:
-                response = request("GET", endpoint, headers=headers, retries=1)
+    def test_user_agent_header_with_empty_value(self):
+        """测试User-Agent头部设置为空字符串时的行为"""
+        # 显式设置User-Agent为空字符串
+        headers = {"User-Agent": ""}
 
-                if response.status == 200:
-                    response_data = json.loads(response.body)
-
-                    # 不同的测试站点响应格式可能略有不同
-                    if "headers" in response_data:
-                        response_headers = response_data["headers"]
-                        user_agent_key = None
-                        # 查找User-Agent头部（不区分大小写）
-                        for key in response_headers:
-                            if key.lower() == "user-agent":
-                                user_agent_key = key
-                                break
-
-                        if user_agent_key:
-                            self.assertEqual(response_headers[user_agent_key], custom_ua)
-                            self.assertNotEqual(response_headers[user_agent_key], USER_AGENT)
-                            return  # 测试成功，退出
-                    elif "user-agent" in response_data:
-                        # httpbin.org/user-agent 的格式
-                        self.assertEqual(response_data["user-agent"], custom_ua)
-                        self.assertNotEqual(response_data["user-agent"], USER_AGENT)
-                        return  # 测试成功，退出
-
-            except Exception as e:
-                # 记录当前端点失败，继续尝试下一个
-                error_msg = str(e).lower()
-                network_keywords = ["timeout", "connection", "resolution", "unreachable", "network"]
-                if not any(keyword in error_msg for keyword in network_keywords):
-                    # 如果不是网络问题，重新抛出异常
-                    raise
-                continue
-
-        # 所有端点都失败
-        self.skipTest("All test endpoints unavailable for case-insensitive user-agent test")
+        if not self._test_user_agent_with_endpoints(headers=headers, expected_ua=""):
+            self.skipTest("All test endpoints unavailable or empty User-Agent causes expected failures")
 
 
 class TestHttpResponse(unittest.TestCase):
@@ -512,7 +441,7 @@ def test_http_post_redirect(self):
         from ddns.util.http import request
 
         try:
-            redirect_url = "http://httpbin.org/redirect-to?url=http://httpbin.org/get"
+            redirect_url = "http://httpbingo.org/redirect-to?url=/get"
             post_data = "test=data&method=POST->GET"
             response_post = request("POST", redirect_url, data=post_data, verify=False, retries=3)
 
@@ -523,7 +452,7 @@ def test_http_post_redirect(self):
             # 验证最终到达了GET端点
             data_post = json.loads(response_post.body)
             self.assertIn("url", data_post)
-            self.assertIn("httpbin.org/get", data_post["url"])
+            self.assertIn(".org/get", data_post["url"])
 
         except Exception as e:
             # 网络问题时跳过测试
@@ -535,43 +464,6 @@ def test_http_post_redirect(self):
                 # 其他异常重新抛出
                 raise
 
-    def test_basic_auth_with_embedded_url(self):
```

## C016: graphql-python/graphql-server#134 (OpenAI_Codex, merged yes)

Enable Chalice multipart uploads

Commit f852c3893d: Applied formatting

File src/tests/test/test_runtime.py:

```diff
     from graphql.validation.rules.no_unused_fragments import NoUnusedFragmentsRule
 
-    doc = parse('query Test { hello }')
+    doc = parse("query Test { hello }")
     assert runtime.validate_document(schema, doc, (NoUnusedFragmentsRule,)) == []
 
 
 def test_get_custom_context_kwargs(monkeypatch):
-    assert runtime._get_custom_context_kwargs({'a': 1}) == {'operation_extensions': {'a': 1}}
-    monkeypatch.setattr(runtime, 'IS_GQL_33', False)
+    assert runtime._get_custom_context_kwargs({"a": 1}) == {
+        "operation_extensions": {"a": 1}
+    }
+    monkeypatch.setattr(runtime, "IS_GQL_33", False)
     try:
-        assert runtime._get_custom_context_kwargs({'a': 1}) == {}
+        assert runtime._get_custom_context_kwargs({"a": 1}) == {}
     finally:
-        monkeypatch.setattr(runtime, 'IS_GQL_33', True)
+        monkeypatch.setattr(runtime, "IS_GQL_33", True)
 
 
 def test_get_operation_type_multiple_operations():
-    doc = parse('query A{hello} query B{hello}')
+    doc = parse("query A{hello} query B{hello}")
```

## C017: charlesvestal/extending-move#38 (OpenAI_Codex, merged no)

Implement HTML file browser for preset tools

Commit 132b08c1b2: Add lazy-loading file browser

File tests/test_flask_routes.py:

```diff
     move_webserver.app.config['TESTING'] = True
     return move_webserver.app.test_client()
 
-def test_reverse_get(client, monkeypatch):
-    monkeypatch.setattr(move_webserver, 'get_wav_files', lambda d: ['sample.wav'])
+def test_reverse_get(client):
     resp = client.get('/reverse')
     assert resp.status_code == 200
-    assert b'sample.wav' in resp.data
+    assert b'class="file-browser"' in resp.data
 
 def test_reverse_post(client, monkeypatch):
     def fake_handle_post(form):
@@ -84,42 +83,43 @@ def fake_post(form):
         return {
             'message': 'saved',
             'message_type': 'success',
-            'options': '<option value="x" selected>Sub/preset (Drift)</option>',
             'macros_html': '<p>done</p>',
             'selected_preset': 'x',
+            'browser_root': '/tmp',
         }
     monkeypatch.setattr(move_webserver.synth_handler, 'handle_post', fake_post)
     resp = client.post('/synth-macros', data={'action': 'select_preset'})
     assert resp.status_code == 200
     assert b'saved' in resp.data
-    assert b'name="preset_select" value="x"' in resp.data
-    assert b'id="preset_select"' in resp.data and b'disabled' in resp.data
     assert b'Choose Another Preset' in resp.data
+    assert b'<p>done</p>' in resp.data
 
 def test_drum_rack_inspector_get(client, monkeypatch):
     def fake_get():
         return {
-            'options': '<option value="1">P</option>',
+            'file_browser_html': '<ul></ul>',
             'message': '',
-            'samples_html': ''
+            'samples_html': '',
+            'browser_root': '/tmp'
         }
     monkeypatch.setattr(move_webserver.drum_rack_handler, 'handle_get', fake_get)
     resp = client.get('/drum-rack-inspector')
     assert resp.status_code == 200
-    assert b'<option value="1">P</option>' in resp.data
+    assert b'class="file-browser"' in resp.data
 
 def test_drum_rack_inspector_post(client, monkeypatch):
     def fake_post(form):
         return {
             'message': 'ok',
             'message_type': 'success',
-            'options': '<option value="1">P</option>',
-            'samples_html': '<div>grid</div>'
+            'samples_html': '<div>grid</div>',
+            'browser_root': '/tmp',
+            'selected_preset': 'x',
         }
     monkeypatch.setattr(move_webserver.drum_rack_handler, 'handle_post', fake_post)
     resp = client.post('/drum-rack-inspector', data={'action':'select_preset', 'preset_select':'x'})
     assert resp.status_code == 200
-    assert b'grid' in resp.data
+    assert b'<div>grid</div>' in resp.data
 
 def test_chord_get(client):
     resp = client.get('/chord')
```

## C024: swingerman/ha-dual-smart-thermostat#426 (Copilot, merged no)

Add Playwright E2E tests for config &amp; options flows (Phase 1A) - Merged with Docker Infrastructure

Commit ac446416a0: Fix min-cycle-duration and keep-alive options (#405)

File tests/test_cooler_mode.py:

```diff
     setup_comp_1,
     setup_comp_heat_ac_cool,
     setup_comp_heat_ac_cool_cycle,
-    setup_comp_heat_ac_cool_cycle_kepp_alive,
     setup_comp_heat_ac_cool_fan_config,
     setup_comp_heat_ac_cool_presets,
     setup_comp_heat_ac_cool_presets_range,
@@ -680,183 +679,125 @@ async def test_no_state_change_when_operation_mode_off_2(
     assert len(calls) == 0
 
 
-async def test_temp_change_ac_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_temp_change_ac_trigger_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn ac on."""
-    calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    """Test if temperature change turn ac on or off."""
+    calls = setup_switch(hass, sw_on)
+    await common.async_set_temperature(hass, 28)
+    setup_sensor(hass, 30 if sw_on else 25)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
-
-async def test_temp_change_ac_trigger_on_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_SWITCH
-
 
-async def test_temp_change_ac_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # set temperature to switch
+    setup_sensor(hass, 25 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # no call, not enought time
     assert len(calls) == 0
 
+    # move back to no switch temp
+    setup_sensor(hass, 30 if sw_on else 25)
+    await hass.async_block_till_done()
 
-async def test_temp_change_ac_trigger_off_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    # no call, not needed
+    assert len(calls) == 0
 
-async def test_mode_change_ac_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # set temperature to switch
+    setup_sensor(hass, 25 if sw_on else 30)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_mode_change_ac_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_ac_trigger_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_cycle,  # noqa: F811
 ) -> None:
-    """Test if mode change turns ac on despite minimum cycle."""
-    calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    """Test if temperature change turn ac on or off when cycle time is past."""
+    calls = setup_switch(hass, sw_on)
+    await common.async_set_temperature(hass, 28)
+    setup_sensor(hass, 30 if sw_on else 25)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
-async def test_temp_change_ac_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # set temperature to switch
+    setup_sensor(hass, 25 if sw_on else 30)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    # no call, not enought time
+    assert len(calls) == 0
 
-async def test_temp_change_ac_trigger_on_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # complete cycle time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
+
+    # call triggered, time is enought
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_ac_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_mode_change_ac_trigger_not_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn ac on."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    """Test if mode change turns ac off or on despite minimum cycle."""
+    calls = setup_switch(hass, sw_on)
+    await common.async_set_temperature(hass, 28)
+    setup_sensor(hass, 30 if sw_on else 25)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-
 
-async def test_temp_change_ac_trigger_off_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
-
 
-async def test_mode_change_ac_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # set temperature to switch
+    setup_sensor(hass, 25 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # no call, not enought time
     assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    # change HVAC mode
+    await common.async_set_hvac_mode(hass, HVACMode.OFF if sw_on else HVACMode.COOL)
 
-async def test_mode_change_ac_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac on despite minimum cycle."""
-    calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
-    await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
     assert len(calls) == 1
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
```

Commit ac446416a0: Fix min-cycle-duration and keep-alive options (#405)

File tests/test_dry_mode.py:

```diff
 ) -> None:
     """Test if humidity change turn dryer on."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
+    calls = setup_switch_dual(hass, common.ENT_DRYER, False, sw_on)
     await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 71)
+    setup_humidity_sensor(hass, 71 if sw_on else 50)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-
 
-async def test_temp_change_ac_dry_trigger_on_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if humidity change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 71)
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_DRYER
-
 
-async def test_temp_change_ac_dry_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if humidity change turn ac on."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 71)
+    # set humidity to switch
+    setup_humidity_sensor(hass, 50 if sw_on else 71)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    # no call, not enought time
+    assert len(calls) == 0
 
-async def test_temp_change_ac_dry_trigger_off_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if himidity change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch_dual(hass, common.ENT_DRYER, False, True)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 50)
+    # move back to no switch humidity
+    setup_humidity_sensor(hass, 71 if sw_on else 50)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_DRYER
 
-
-async def test_mode_change_ac_dry_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, True)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 50)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_DRYER
-
 
-async def test_mode_change_ac_dry_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac on despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 70)
-    await hass.async_block_till_done()
+    # no call, not needed
     assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.DRY)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_DRYER
-
 
-async def test_temp_change_ac_dry_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if humidity change turn ac on."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 70)
+    # set humidity to switch
+    setup_humidity_sensor(hass, 50 if sw_on else 71)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
-
-async def test_temp_change_ac_dryer_trigger_on_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if humidity change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 70)
-    await hass.async_block_till_done()
+    # call triggered, time is enought and humidity reached
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_DRYER
 
 
-async def test_temp_change_ac_dry_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_ac_dry_trigger_on_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_dry_cycle,  # noqa: F811
 ) -> None:
-    """Test if humidity change turn ac on."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, True)
+    """Test if humidity change turn dryer on when cycle time is past."""
+    calls = setup_switch_dual(hass, common.ENT_DRYER, False, sw_on)
     await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 50)
+    setup_humidity_sensor(hass, 71 if sw_on else 50)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
-async def test_temp_change_ac_dry_trigger_off_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if humidity change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch_dual(hass, common.ENT_DRYER, False, True)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 50)
+    # set humidity to switch
+    setup_humidity_sensor(hass, 50 if sw_on else 71)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_DRYER
 
+    # no call, not enought time
+    assert len(calls) == 0
 
-async def test_mode_change_ac_dry_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, True)
-    await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 50)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
+
+    # call triggered, time is enought and humidity reached
     assert len(calls) == 1
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_DRYER
 
 
-async def test_mode_change_ac_dry_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_mode_change_ac_dry_trigger_off_not_long_enough(
+    hass: HomeAssistant, sw_on, setup_comp_heat_ac_cool_dry_cycle  # noqa: F811
 ) -> None:
-    """Test if mode change turns ac on despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_DRYER, False, False)
+    """Test if mode change turns dryer despite minimum cycle."""
+    calls = setup_switch_dual(hass, common.ENT_DRYER, False, sw_on)
     await common.async_set_humidity(hass, 65)
-    setup_humidity_sensor(hass, 70)
+    setup_humidity_sensor(hass, 50 if sw_on else 71)
     await hass.async_block_till_done()
     assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.DRY)
+    await common.async_set_hvac_mode(hass, HVACMode.OFF if sw_on else HVACMode.DRY)
     assert len(calls) == 1
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_DRYER
 
 
```

Commit ac446416a0: Fix min-cycle-duration and keep-alive options (#405)

File tests/test_fan_mode.py:

```diff
-    setup_comp_heat_ac_cool_cycle_kepp_alive,
     setup_comp_heat_ac_cool_fan_config,
     setup_comp_heat_ac_cool_fan_config_cycle,
+    setup_comp_heat_ac_cool_fan_config_keep_alive,
     setup_comp_heat_ac_cool_fan_config_presets,
     setup_comp_heat_ac_cool_fan_config_tolerance,
     setup_comp_heat_ac_cool_fan_config_tolerance_min_cycle,
@@ -1059,564 +1057,445 @@ async def test_no_state_cooler_fan_change_when_operation_mode_off_2(
     assert len(calls) == 0
 
 
-async def test_temp_change_fan_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_temp_change_fan_trigger_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_fan_only_config_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    calls = setup_switch(hass, False)
+    """Test if temperature change turn fan on or off."""
+    calls = setup_switch(hass, sw_on)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 30 if sw_on else 23)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
-async def test_temp_change_cooler_fan_ac_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # no call, not enought time
     assert len(calls) == 0
 
+    # move back to no switch temp
+    setup_sensor(hass, 30 if sw_on else 23)
+    await hass.async_block_till_done()
 
-async def test_temp_change_cooler_fan_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    # no call, not needed
+    assert len(calls) == 0
 
-async def test_temp_change_fan_trigger_on_long_enough(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn fan on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_cooler_fan_ac_trigger_on_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_fan_trigger_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_fan_only_config_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        await common.async_set_hvac_mode(hass, HVACMode.COOL)
-        calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
+    """Test if temperature change turn fan on or off when cycle time is past."""
+    calls = setup_switch(hass, sw_on)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 30 if sw_on else 23)
+    await hass.async_block_till_done()
+
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
+
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
+    await hass.async_block_till_done()
+
+    # no call, not enought time
+    assert len(calls) == 0
+
+    # complete cycle time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_cooler_fan_trigger_on_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_mode_change_fan_trigger_not_long_enough(
+    hass: HomeAssistant, sw_on, setup_comp_fan_only_config_cycle  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-        calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
+    """Test if mode change turns fan despite minimum cycle."""
+    calls = setup_switch(hass, sw_on)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 20 if sw_on else 30)
     await hass.async_block_till_done()
+    assert len(calls) == 0
+    await common.async_set_hvac_mode(hass, HVACMode.OFF if sw_on else HVACMode.FAN_ONLY)
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_FAN
-
-
-async def test_temp_change_fan_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn fan on."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
-    await hass.async_block_till_done()
-    assert len(calls) == 0
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
+    assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_cooler_fan_ac_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_temp_change_cooler_fan_ac_trigger_on_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_fan_config_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn ac on."""
+    """Test if temperature change turn ac on or off."""
     await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    calls = setup_switch_dual(hass, common.ENT_FAN, True, False)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    calls = setup_switch_dual(hass, common.ENT_FAN, sw_on, False)
+    await common.async_set_temperature(hass, 25)
+    setup_sensor(hass, 30 if sw_on else 23)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
-async def test_temp_change_cooler_fan_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn fan on."""
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # no call, not enought time
     assert len(calls) == 0
 
+    # move back to no switch temp
+    setup_sensor(hass, 30 if sw_on else 23)
+    await hass.async_block_till_done()
 
-async def test_temp_change_fan_trigger_off_long_enough(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    # no call, not needed
+    assert len(calls) == 0
 
-async def test_temp_change_cooler_fan_ac_trigger_off_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        await common.async_set_hvac_mode(hass, HVACMode.COOL)
-        calls = setup_switch_dual(hass, common.ENT_FAN, True, False)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_cooler_fan_trigger_off_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_cooler_fan_ac_trigger_on_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_fan_config_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-        calls = setup_switch_dual(hass, common.ENT_FAN, False, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    """Test if temperature change turn ac on or off when cycle time is past."""
+    await common.async_set_hvac_mode(hass, HVACMode.COOL)
+    calls = setup_switch_dual(hass, common.ENT_FAN, sw_on, False)
+    await common.async_set_temperature(hass, 25)
+    setup_sensor(hass, 30 if sw_on else 23)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_FAN
 
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
-async def test_mode_change_fan_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns fan off despite minimum cycle."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    # no call, not enought time
+    assert len(calls) == 0
 
-async def test_mode_change_cooler_fan_ac_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    calls = setup_switch_dual(hass, common.ENT_FAN, True, False)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_mode_change_cooler_fan_trigger_off_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_temp_change_cooler_fan_trigger_on_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_fan_config_cycle,  # noqa: F811
 ) -> None:
-    """Test if mode change turns fan off despite minimum cycle."""
+    """Test if temperature change turn fan on or off."""
     await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    calls = setup_switch_dual(hass, common.ENT_FAN, False, sw_on)
+    await common.async_set_temperature(hass, 25)
+    setup_sensor(hass, 30 if sw_on else 23)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_FAN
 
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
-async def test_mode_change_fan_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns fan on despite minimum cycle."""
-    calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
+
+    # no call, not enought time
     assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    # move back to no switch temp
+    setup_sensor(hass, 30 if sw_on else 23)
+    await hass.async_block_till_done()
 
-async def test_mode_change_cooler_fan_ac_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac on despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
+    # no call, not needed
+    assert len(calls) == 0
 
-async def test_mode_change_cooler_fan_trigger_on_not_long_enough(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns fan on despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_FAN
 
 
-async def test_temp_change_fan_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_cooler_fan_trigger_on_long_enough(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_fan_config_cycle,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    calls = setup_switch(hass, False)
+    """Test if temperature change turn fan on or off when cycle time is past."""
+    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
+    calls = setup_switch_dual(hass, common.ENT_FAN, False, sw_on)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 30 if sw_on else 23)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
-
-async def test_temp_change_cooler_fan_ac_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    freezer.tick(timedelta(minutes=6))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-
 
-async def test_temp_change_cooler_fan_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # set temperature to switch
+    setup_sensor(hass, 23 if sw_on else 30)
     await hass.async_block_till_done()
-    assert len(calls) == 0
 
+    # no call, not enought time
+    assert len(calls) == 0
 
-async def test_temp_change_fan_trigger_on_long_enough_2(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn fan on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    # go over cycle time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
+
+    # call triggered, time is enought and temp reached
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_SWITCH
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
+    assert call.data["entity_id"] == common.ENT_FAN
 
 
-async def test_temp_change_cooler_fan_ac_trigger_on_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_mode_change_cooler_fan_ac_trigger_off_not_long_enough(
+    hass: HomeAssistant, sw_on, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
 ) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-        await common.async_set_hvac_mode(hass, HVACMode.COOL)
+    """Test if mode change turns ac despite minimum cycle."""
+    await common.async_set_hvac_mode(hass, HVACMode.COOL if sw_on else HVACMode.OFF)
+    calls = setup_switch_dual(hass, common.ENT_FAN, sw_on, False)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 20 if sw_on else 30)
     await hass.async_block_till_done()
+    assert len(calls) == 0
+    await common.async_set_hvac_mode(hass, HVACMode.OFF if sw_on else HVACMode.COOL)
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_cooler_fan_trigger_on_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_mode_change_cooler_fan_trigger_off_not_long_enough(
+    hass: HomeAssistant, sw_on, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-        await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
+    """Test if mode change turns fan despite minimum cycle."""
+    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY if sw_on else HVACMode.OFF)
+    calls = setup_switch_dual(hass, common.ENT_FAN, False, sw_on)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 20 if sw_on else 30)
     await hass.async_block_till_done()
+    assert len(calls) == 0
+    await common.async_set_hvac_mode(hass, HVACMode.OFF if sw_on else HVACMode.FAN_ONLY)
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_ON
+    assert call.service == SERVICE_TURN_OFF if sw_on else SERVICE_TURN_ON
     assert call.data["entity_id"] == common.ENT_FAN
 
 
-async def test_temp_change_fan_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_fan_trigger_keep_alive(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_fan_only_config_keep_alive,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    """Test turn fan on or off when keep alive time is past."""
+    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY if sw_on else HVACMode.OFF)
+    calls = setup_switch(hass, sw_on)
+    await common.async_set_temperature(hass, 25)
+    setup_sensor(hass, 30 if sw_on else 23)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-
 
-async def test_temp_change_cooler_fan_ac_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    calls = setup_switch_dual(hass, common.ENT_FAN, True, False)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-
 
-async def test_temp_change_cooler_fan_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn fan on."""
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
-    await hass.async_block_till_done()
+    # no call, not enought time
     assert len(calls) == 0
 
-
-async def test_temp_change_fan_trigger_off_long_enough_2(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # complete keep-alive time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
-
 
-async def test_temp_change_cooler_fan_ac_trigger_off_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if temperature change turn ac on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        await common.async_set_hvac_mode(hass, HVACMode.COOL)
-        calls = setup_switch_dual(hass, common.ENT_FAN, True, False)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
-    await hass.async_block_till_done()
+    # keep-alive call triggered, time is enought
     assert len(calls) == 1
     call = calls[0]
     assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
+    assert call.service == SERVICE_TURN_ON if sw_on else SERVICE_TURN_OFF
     assert call.data["entity_id"] == common.ENT_SWITCH
 
 
-async def test_temp_change_cooler_fan_trigger_off_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_ac_trigger_keep_alive(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_fan_config_keep_alive,  # noqa: F811
 ) -> None:
-    """Test if temperature change turn fan on."""
-    fake_changed = datetime.datetime(1970, 11, 11, 11, 11, 11, tzinfo=dt_util.UTC)
-    with freeze_time(fake_changed):
-        await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-        calls = setup_switch_dual(hass, common.ENT_FAN, False, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    """Test turn ac on or off when keep alive time is past."""
+    await common.async_set_hvac_mode(hass, HVACMode.COOL if sw_on else HVACMode.OFF)
+    calls = setup_switch_dual(hass, common.ENT_FAN, sw_on, False)
+    await common.async_set_temperature(hass, 25)
+    setup_sensor(hass, 30 if sw_on else 20)
     await hass.async_block_till_done()
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == HASS_DOMAIN
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_FAN
 
-
-async def test_mode_change_fan_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    calls = setup_switch(hass, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
 
-
-async def test_mode_change_cooler_fan_ac_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns ac off despite minimum cycle."""
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    calls = setup_switch_dual(hass, common.ENT_FAN, True, False)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
-    await hass.async_block_till_done()
+    # no call, not enought time
     assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_SWITCH
-
 
-async def test_mode_change_cooler_fan_trigger_off_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns fan off despite minimum cycle."""
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, True)
-    await common.async_set_temperature(hass, 30)
-    setup_sensor(hass, 25)
+    # complete keep-alive time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.OFF)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_OFF
-    assert call.data["entity_id"] == common.ENT_FAN
-
 
-async def test_mode_change_fan_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_fan_only_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns fan on despite minimum cycle."""
-    calls = setup_switch(hass, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
-    await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    assert len(calls) == 1
+    # keep-alive call triggered, time is enought
+    # on turn off we have 2 call, 1 per switch
+    assert len(calls) == 1 if sw_on else 2
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_ON if sw_on else SERVICE_TURN_OFF
     assert call.data["entity_id"] == common.ENT_SWITCH
+    if len(calls) == 2:
+        call = calls[1]
+        assert call.domain == HASS_DOMAIN
+        assert call.service == SERVICE_TURN_OFF
+        assert call.data["entity_id"] == common.ENT_FAN
 
 
-async def test_mode_change_cooler_fan_ac_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
<email>.parametrize("sw_on", [True, False])
<email>.parametrize("expected_lingering_timers", [True])
+async def test_time_change_ac_fan_trigger_keep_alive(
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    sw_on,
+    setup_comp_heat_ac_cool_fan_config_keep_alive,  # noqa: F811
 ) -> None:
-    """Test if mode change turns ac on despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
+    """Test turn fan on or off when keep alive time is past."""
+    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY if sw_on else HVACMode.OFF)
+    calls = setup_switch_dual(hass, common.ENT_FAN, False, sw_on)
     await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    setup_sensor(hass, 30 if sw_on else 20)
     await hass.async_block_till_done()
-    assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.COOL)
-    assert len(calls) == 1
-    call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_SWITCH
-
 
-async def test_mode_change_cooler_fan_trigger_on_not_long_enough_2(
-    hass: HomeAssistant, setup_comp_heat_ac_cool_fan_config_cycle  # noqa: F811
-) -> None:
-    """Test if mode change turns fan on despite minimum cycle."""
-    calls = setup_switch_dual(hass, common.ENT_FAN, False, False)
-    await common.async_set_temperature(hass, 25)
-    setup_sensor(hass, 30)
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
     await hass.async_block_till_done()
+
+    # no call, not enought time
     assert len(calls) == 0
-    await common.async_set_hvac_mode(hass, HVACMode.FAN_ONLY)
-    assert len(calls) == 1
+
+    # complete keep-alive time
+    freezer.tick(timedelta(minutes=5))
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
+
+    # keep-alive call triggered, time is enought
+    # on turn off we have 2 call, 1 per switch
+    assert len(calls) == 1 if sw_on else 2
     call = calls[0]
-    assert call.domain == "homeassistant"
-    assert call.service == SERVICE_TURN_ON
-    assert call.data["entity_id"] == common.ENT_FAN
+    assert call.domain == HASS_DOMAIN
+    assert call.service == SERVICE_TURN_ON if sw_on else SERVICE_TURN_OFF
+    assert call.data["entity_id"] == common.ENT_FAN if sw_on else common.ENT_SWITCH
+    if len(calls) == 2:
+        call = calls[1]
+        assert call.domain == HASS_DOMAIN
+        assert call.service == SERVICE_TURN_OFF
+        assert call.data["entity_id"] == common.ENT_FAN
 
 
 async def test_fan_mode(hass: HomeAssistant, setup_comp_1) -> None:  # noqa: F811
@@ -2187,9 +2066,13 @@ async def test_cooler_fan_ac_and_mode(
         (timedelta(seconds=30), STATE_OFF),
     ],
 )
<email>.asyncio
<email>.parametrize("expected_lingering_timers", [True])
 async def test_fan_mode_cycle(
-    hass: HomeAssistant, duration, result_state, setup_comp_1  # noqa: F811
+    hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
+    duration,
+    result_state,
+    setup_comp_1,  # noqa: F811
 ) -> None:
     """Test thermostat cooler switch in cooling mode with cycle duration."""
     cooler_switch = "input_boolean.test"
@@ -2229,11 +2112,13 @@ async def test_fan_mode_cycle(
     setup_sensor(hass, 23)
     await hass.async_block_till_done()
 
-    fake_changed = dt.utcnow() - duration
-    with freeze_time(fake_changed):
-        await common.async_set_temperature(hass, 18)
-        await hass.async_block_till_done()
-        assert hass.states.get(cooler_switch).state == STATE_ON
+    await common.async_set_temperature(hass, 18)
+    await hass.async_block_till_done()
+    assert hass.states.get(cooler_switch).state == STATE_ON
+
+    freezer.tick(duration)
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
     setup_sensor(hass, 17)
     await hass.async_block_till_done()
@@ -2249,9 +2134,10 @@ async def test_fan_mode_cycle(
         (timedelta(seconds=30), HVACMode.FAN_ONLY, STATE_OFF, STATE_OFF),
     ],
 )
<email>.asyncio
<email>.parametrize("expected_lingering_timers", [True])
 async def test_cooler_fan_mode_cycle(
     hass: HomeAssistant,
+    freezer: FrozenDateTimeFactory,
     duration,
     hvac_mode,
     cooler_result_state,
@@ -2299,21 +2185,22 @@ async def test_cooler_fan_mode_cycle(
     setup_sensor(hass, 23)
     await hass.async_block_till_done()
 
-    fake_changed = dt.utcnow() - duration
-    with freeze_time(fake_changed):
+    await common.async_set_temperature(hass, 18)
+    await hass.async_block_till_done()
+    assert (
+        hass.states.get(cooler_switch).state == STATE_ON
+        if hvac_mode == HVACMode.COOL
+        else STATE_OFF
+    )
+    assert (
+        hass.states.get(fan_switch).state == STATE_OFF
+        if hvac_mode == HVACMode.COOL
+        else STATE_ON
+    )
 
-        await common.async_set_temperature(hass, 18)
-        await hass.async_block_till_done()
-        assert (
-            hass.states.get(cooler_switch).state == STATE_ON
-            if hvac_mode == HVACMode.COOL
-            else STATE_OFF
-        )
-        assert (
-            hass.states.get(fan_switch).state == STATE_OFF
-            if hvac_mode == HVACMode.COOL
-            else STATE_ON
-        )
+    freezer.tick(duration)
+    common.async_fire_time_changed(hass)
+    await hass.async_block_till_done()
 
     setup_sensor(hass, 17)
     await hass.async_block_till_done()
@@ -2358,6 +2245,7 @@ async def test_set_target_temp_ac_fan_on(
     assert call.data["entity_id"] == common.ENT_FAN
 
 
<email>.parametrize("expected_lingering_timers", [True])
 async def test_set_target_temp_ac_on_tolerance_and_cycle(
     hass: HomeAssistant, setup_comp_1  # noqa: F811
 ) -> None:
@@ -2466,6 +2354,7 @@ async def test_set_target_temp_ac_on_after_fan_tolerance(
     assert call.data["entity_id"] == common.ENT_FAN
 
 
<email>.parametrize("expected_lingering_timers", [True])
 async def test_set_target_temp_ac_on_dont_switch_to_fan_during_cycle1(
     hass: HomeAssistant,
 ) -> None:
@@ -2499,6 +2388,7 @@ async def test_set_target_temp_ac_on_dont_switch_to_fan_during_cycle1(
     )
 
 
<email>.parametrize("expected_lingering_timers", [True])
 async def test_set_target_temp_ac_on_dont_switch_to_fan_during_cycle2(
     hass: HomeAssistant,
 ) -> None:
@@ -2518,16 +2408,19 @@ async def test_set_target_temp_ac_on_dont_switch_to_fan_during_cycle2(
     assert len(calls) == 0
 
 
<email>.parametrize("expected_lingering_timers", [True])
 async def test_set_target_temp_ac_on_dont_switch_to_fan_during_cycle3(
-    hass: HomeAssistant,
+    hass: HomeAssistant, freezer: FrozenDateTimeFactory
 ) -> None:
     """Test if switched to fan because min_cycle_duration reached."""
```

## C030: microsoft/Qcodes#7240 (Copilot, merged yes)

Fix inferred parameters missing from dataset when explicitly added

Commit 1b9fc126c9: Enhanced test coverage for inferred parameters fix

File tests/dataset/measurement/test_inferred_parameters_fix.py:

```diff
         
-        # Get parameter data - both parameters should be present
+        # Get parameter data - all parameters should be present
         param_data = dataset.get_parameter_data()
         
-        # Both parameters should be in the dataset
+        # All parameters should be in the dataset
         assert "dac_ch1" in param_data, "dac_ch1 should be in parameter data"
-        assert "del_param_1" in param_data, "del_param_1 should be in parameter data"
+        assert "del_param_1" in param_data, "del_param_1 should be in parameter data"  
+        assert "standalone" in param_data, "standalone parameter should be in parameter data"
         
         # Check that the data is correct
         assert len(param_data["dac_ch1"]["dac_ch1"]) == 1
-        assert len(param_data["del_param_1"]["del_param_1"]) == 1
\ No newline at end of file
+        assert len(param_data["del_param_1"]["del_param_1"]) == 1
+        assert len(param_data["standalone"]["standalone"]) == 1
\ No newline at end of file
```

Commit bef75efa23: Run precommit hooks

File tests/dataset/measurement/test_inferred_parameters_fix.py:

```diff
-        
+
         # Get parameter data - all parameters should be present
         param_data = dataset.get_parameter_data()
-        
+
         # All parameters should be in the dataset
         assert "dac_ch1" in param_data, "dac_ch1 should be in parameter data"
-        assert "del_param_1" in param_data, "del_param_1 should be in parameter data"  
-        assert "standalone" in param_data, "standalone parameter should be in parameter data"
-        
+        assert "del_param_1" in param_data, "del_param_1 should be in parameter data"
+        assert "standalone" in param_data, (
+            "standalone parameter should be in parameter data"
+        )
+
         # Check that the data is correct
         assert len(param_data["dac_ch1"]["dac_ch1"]) == 1
         assert len(param_data["del_param_1"]["del_param_1"]) == 1
@@ -145,77 +151,73 @@ def test_multiple_dependent_parameters_no_cross_contamination():
```

Commit dcd1a36875: Use the tmp_path fixture in tests

File tests/dataset/measurement/test_inferred_parameters_fix.py:

```diff
-        )  # depends on del_param_1
-
-        # Verify the interdependencies are set up correctly
-        interdeps = meas._interdeps
-
-        # Check that we have the expected structure
-        assert len(interdeps.dependencies) == 1  # measurement depends on del_param_1
-        assert len(interdeps.inferences) == 1  # del_param_1 inferred from dac_ch1
-        assert len(interdeps.standalones) == 1  # dac_ch1 is standalone
-
-        # Get the parameter specs
-        measurement_spec = interdeps._id_to_paramspec["measurement"]
-        del_param_spec = interdeps._id_to_paramspec["del_param_1"]
-        dac_spec = interdeps._id_to_paramspec["dac_ch1"]
-
-        # Test the collect_all_related_parameters method directly
-
-        # Simulate a result_dict that would be passed to _enqueue_results
-        result_dict = {measurement_spec: [1.0], del_param_spec: [0.5], dac_spec: [0.1]}
-
-        # Test the helper method
-        initial_params = {measurement_spec, del_param_spec}
-        collected = interdeps.collect_all_related_parameters(initial_params)
-        # Filter to only include parameters that are in result_dict (same as the original behavior)
-        collected = collected.intersection(result_dict.keys())
-
-        # Verify that all three parameters are collected
-        collected_names = {p.name for p in collected}
-        expected_names = {"measurement", "del_param_1", "dac_ch1"}
-        assert collected_names == expected_names, (
-            f"Expected {expected_names}, got {collected_names}"
-        )
+    # Create a measurement parameter that depends on the delegate parameter
+    measurement_param = Parameter("measurement", get_cmd=lambda: 42.0)
+
+    # Create measurement
+    meas = Measurement(name="test_measurement", exp=exp)
+
+    # Register parameters to create the dependency chain:
+    # measurement depends on del_param_1, del_param_1 is inferred from dac_ch1
+    meas.register_parameter(dac.ch1)  # standalone
+    meas.register_parameter(del_param, basis=(dac.ch1,))  # inferred from dac_ch1
+    meas.register_parameter(
+        measurement_param, setpoints=(del_param,)
+    )  # depends on del_param_1
+
+    # Verify the interdependencies are set up correctly
+    interdeps = meas._interdeps
+
+    # Check that we have the expected structure
+    assert len(interdeps.dependencies) == 1  # measurement depends on del_param_1
+    assert len(interdeps.inferences) == 1  # del_param_1 inferred from dac_ch1
+    assert len(interdeps.standalones) == 0  # dac_ch1 is standalone
+
+    # Get the parameter specs
+    measurement_spec = interdeps._id_to_paramspec["measurement"]
+    del_param_spec = interdeps._id_to_paramspec["del_param_1"]
+    dac_spec = interdeps._id_to_paramspec["dac_ch1"]
+
+    # Test the collect_all_related_parameters method directly
+
+    # Simulate a result_dict that would be passed to _enqueue_results
+    result_dict = {measurement_spec: [1.0], del_param_spec: [0.5], dac_spec: [0.1]}
+
+    # Test the helper method
+    initial_params = {measurement_spec, del_param_spec}
+    collected = interdeps.collect_all_related_parameters(initial_params)
+    # Filter to only include parameters that are in result_dict (same as the original behavior)
+    collected = collected.intersection(result_dict.keys())
+
+    # Verify that all three parameters are collected
+    collected_names = {p.name for p in collected}
+    expected_names = {"measurement", "del_param_1", "dac_ch1"}
+    assert collected_names == expected_names, (
+        f"Expected {expected_names}, got {collected_names}"
+    )
 
 
-def test_inferred_parameters_in_actual_measurement():
+def test_inferred_parameters_in_actual_measurement(tmp_path):
     """
     Test the full measurement flow to ensure inferred parameters are saved correctly.
     """
 
-    with tempfile.TemporaryDirectory() as temp_dir:
-        db_path = Path(temp_dir) / "test.db"
-        initialise_or_create_database_at(db_path)
+    db_path = Path(tmp_path) / "test.db"
+    initialise_or_create_database_at(db_path)
 
-        # Create experiment
-        exp = new_experiment("test_exp", sample_name="test_sample")
+    # Create experiment
+    exp = new_experiment("test_exp", sample_name="test_sample")
 
-        # Create mock instruments
-        dac = DummyInstrument("dac", gates=["ch1"])
+    # Create mock instruments
+    dac = DummyInstrument("dac", gates=["ch1"])
 
-        # Create delegate parameter
-        del_param = DelegateParameter(
-            "del_param_1", label="del param 1", source=dac.ch1
-        )
+    # Create delegate parameter
+    del_param = DelegateParameter("del_param_1", label="del param 1", source=dac.ch1)
+
+    # Create a standalone parameter to test that standalone handling still works
+    standalone_param = Parameter("standalone", get_cmd=lambda: 3.14)
+
+    # Create measurement
+    meas = Measurement(name="test_measurement", exp=exp)
+
+    # Register parameters
+    meas.register_parameter(dac.ch1)  # This should be standalone
+    meas.register_parameter(
+        del_param, basis=(dac.ch1,)
+    )  # This should be inferred from dac.ch1
+    meas.register_parameter(standalone_param)  # This should be standalone
+
+    # Run measurement
+    with meas.run() as datasaver:
+        # Set values and add results
+        dac.ch1.set(0.5)
+        del_param.set(0.5)
+        standalone_param.set(3.14)
 
-        # Create a standalone parameter to test that standalone handling still works
-        standalone_param = Parameter("standalone", get_cmd=lambda: 3.14)
-
-        # Create measurement
-        meas = Measurement(name="test_measurement", exp=exp)
-
-        # Register parameters
-        meas.register_parameter(dac.ch1)  # This should be standalone
-        meas.register_parameter(
-            del_param, basis=(dac.ch1,)
-        )  # This should be inferred from dac.ch1
-        meas.register_parameter(standalone_param)  # This should be standalone
-
-        # Run measurement
-        with meas.run() as datasaver:
-            # Set values and add results
-            dac.ch1.set(0.5)
-            del_param.set(0.5)
-            standalone_param.set(3.14)
-
-            datasaver.add_result(
-                (dac.ch1, dac.ch1()),
-                (del_param, del_param()),
-                (standalone_param, standalone_param()),
-            )
-
-        # Retrieve the dataset
-        dataset = datasaver.dataset
-
-        # Get parameter data - all parameters should be present
-        param_data = dataset.get_parameter_data()
-
-        # All parameters should be in the dataset
-        assert "dac_ch1" in param_data, "dac_ch1 should be in parameter data"
-        assert "del_param_1" in param_data, "del_param_1 should be in parameter data"
-        assert "standalone" in param_data, (
-            "standalone parameter should be in parameter data"
+        datasaver.add_result(
+            (dac.ch1, dac.ch1()),
+            (del_param, del_param()),
+            (standalone_param, standalone_param()),
         )
 
-        # Check that the data is correct
-        assert len(param_data["dac_ch1"]["dac_ch1"]) == 1
-        assert len(param_data["del_param_1"]["del_param_1"]) == 1
-        assert len(param_data["standalone"]["standalone"]) == 1
+    # Retrieve the dataset
+    dataset = datasaver.dataset
 
+    # Get parameter data - all parameters should be present
+    param_data = dataset.get_parameter_data()
 
-def test_multiple_dependent_parameters_no_cross_contamination():
+    # All parameters should be in the dataset
+    assert "dac_ch1" in param_data, "dac_ch1 should be in parameter data"
+    assert "del_param_1" in param_data, "del_param_1 should be in parameter data"
+    assert "standalone" in param_data, (
+        "standalone parameter should be in parameter data"
+    )
+
+    # Check that the data is correct
+    assert len(param_data["dac_ch1"]["dac_ch1"]) == 1
+    assert len(param_data["del_param_1"]["del_param_1"]) == 1
+    assert len(param_data["standalone"]["standalone"]) == 1
```

## C037: reflex-dev/reflex#5555 (Devin, merged yes)

Refactor AppHarness to use reflex run subprocess instead of threads

Commit e20c257b8c: human fixups

File tests/integration/test_client_storage.py:

```diff
         driver: WebDriver instance.
         local_storage: Local storage helper.
         session_storage: Session storage helper.
+        tmp_path: pytest tmp_path fixture
     """
     app = client_side.app_instance
     assert app is not None
@@ -535,8 +546,8 @@ def set_sub_sub(var: str, value: str):
     assert s1s.text == "s1s value"
 
     # reset the backend state to force refresh from client storage
-    async with client_side.modify_state(f"{token}_{state_name}") as state:
-        state.reset()
+    reset_button = driver.find_element(By.ID, "reset-button")
+    reset_button.click()
     driver.refresh()
 
     # wait for the backend connection to send the token (again)
@@ -652,7 +663,7 @@ def set_sub_sub(var: str, value: str):
             _substate_key(token, sub_sub_state_name)
         )
     elif isinstance(client_side.state_manager, (StateManagerMemory, StateManagerDisk)):
-        del client_side.state_manager.states[token]
+        client_side.state_manager.states.pop(token, None)
     if isinstance(client_side.state_manager, StateManagerDisk):
         client_side.state_manager.token_expiration = 0
         client_side.state_manager._purge_expired_states()
@@ -666,6 +677,7 @@ async def poll_for_not_hydrated():
 
     # Trigger event to get a new instance of the state since the old was expired.
     set_sub("c1", "c1 post expire")
+    set_sub_sub("s1s", "s1s post expire")
 
     # get new references to all cookie and local storage elements (again)
     c1 = driver.find_element(By.ID, "c1")
@@ -702,7 +714,7 @@ async def poll_for_not_hydrated():
     assert s3.text == "s3 value"
     assert c1s.text == "c1s value"
     assert l1s.text == "l1s value"
-    assert s1s.text == "s1s value"
+    assert s1s.text == "s1s post expire"
 
     # Get the backend state and ensure the values are still set
     async def get_sub_state():
@@ -712,11 +724,20 @@ async def get_sub_state():
         state = root_state.substates[client_side.get_state_name("_client_side_state")]
         return state.substates[client_side.get_state_name("_client_side_sub_state")]
 
-    async def poll_for_c1_set():
+    async def get_sub_sub_state():
+        sub_state = await get_sub_state()
+        return sub_state.substates[
+            client_side.get_state_name("_client_side_sub_sub_state")
+        ]
+
+    async def poll_for_post_expire_set():
         sub_state = await get_sub_state()
-        return sub_state.c1 == "c1 post expire"
+        sub_sub_state = await get_sub_sub_state()
+        return (
+            sub_state.c1 == "c1 post expire" and sub_sub_state.s1s == "s1s post expire"
+        )
 
-    assert await AppHarness._poll_for_async(poll_for_c1_set)
+    assert await AppHarness._poll_for_async(poll_for_post_expire_set)
     sub_state = await get_sub_state()
     assert sub_state.c1 == "c1 post expire"
     assert sub_state.c2 == "c2 value"
@@ -732,12 +753,10 @@ async def poll_for_c1_set():
     assert sub_state.s1 == "s1 value"
     assert sub_state.s2 == "s2 value"
     assert sub_state.s3 == "s3 value"
-    sub_sub_state = sub_state.substates[
-        client_side.get_state_name("_client_side_sub_sub_state")
-    ]
+    sub_sub_state = await get_sub_sub_state()
     assert sub_sub_state.c1s == "c1s value"
     assert sub_sub_state.l1s == "l1s value"
-    assert sub_sub_state.s1s == "s1s value"
+    assert sub_sub_state.s1s == "s1s post expire"
 
     # clear the cookie jar and local storage, ensure state reset to default
     driver.delete_all_cookies()
```

Commit 6186d1bc4f: Merge remote changes and fix all darglint errors

File tests/integration/test_client_storage.py:

```diff
         driver: WebDriver instance.
         local_storage: Local storage helper.
         session_storage: Session storage helper.
+        tmp_path: pytest tmp_path fixture
     """
     app = client_side.app_instance
     assert app is not None
@@ -535,8 +546,8 @@ def set_sub_sub(var: str, value: str):
     assert s1s.text == "s1s value"
 
     # reset the backend state to force refresh from client storage
-    async with client_side.modify_state(f"{token}_{state_name}") as state:
-        state.reset()
+    reset_button = driver.find_element(By.ID, "reset-button")
+    reset_button.click()
     driver.refresh()
 
     # wait for the backend connection to send the token (again)
@@ -652,7 +663,7 @@ def set_sub_sub(var: str, value: str):
             _substate_key(token, sub_sub_state_name)
         )
     elif isinstance(client_side.state_manager, (StateManagerMemory, StateManagerDisk)):
-        del client_side.state_manager.states[token]
+        client_side.state_manager.states.pop(token, None)
     if isinstance(client_side.state_manager, StateManagerDisk):
         client_side.state_manager.token_expiration = 0
         client_side.state_manager._purge_expired_states()
@@ -666,6 +677,7 @@ async def poll_for_not_hydrated():
 
     # Trigger event to get a new instance of the state since the old was expired.
     set_sub("c1", "c1 post expire")
+    set_sub_sub("s1s", "s1s post expire")
 
     # get new references to all cookie and local storage elements (again)
     c1 = driver.find_element(By.ID, "c1")
@@ -702,7 +714,7 @@ async def poll_for_not_hydrated():
     assert s3.text == "s3 value"
     assert c1s.text == "c1s value"
     assert l1s.text == "l1s value"
-    assert s1s.text == "s1s value"
+    assert s1s.text == "s1s post expire"
 
     # Get the backend state and ensure the values are still set
     async def get_sub_state():
@@ -712,11 +724,20 @@ async def get_sub_state():
         state = root_state.substates[client_side.get_state_name("_client_side_state")]
         return state.substates[client_side.get_state_name("_client_side_sub_state")]
 
-    async def poll_for_c1_set():
+    async def get_sub_sub_state():
+        sub_state = await get_sub_state()
+        return sub_state.substates[
+            client_side.get_state_name("_client_side_sub_sub_state")
+        ]
+
+    async def poll_for_post_expire_set():
         sub_state = await get_sub_state()
-        return sub_state.c1 == "c1 post expire"
+        sub_sub_state = await get_sub_sub_state()
+        return (
+            sub_state.c1 == "c1 post expire" and sub_sub_state.s1s == "s1s post expire"
+        )
 
-    assert await AppHarness._poll_for_async(poll_for_c1_set)
+    assert await AppHarness._poll_for_async(poll_for_post_expire_set)
     sub_state = await get_sub_state()
     assert sub_state.c1 == "c1 post expire"
     assert sub_state.c2 == "c2 value"
@@ -732,12 +753,10 @@ async def poll_for_c1_set():
     assert sub_state.s1 == "s1 value"
     assert sub_state.s2 == "s2 value"
     assert sub_state.s3 == "s3 value"
-    sub_sub_state = sub_state.substates[
-        client_side.get_state_name("_client_side_sub_sub_state")
-    ]
+    sub_sub_state = await get_sub_sub_state()
     assert sub_sub_state.c1s == "c1s value"
     assert sub_sub_state.l1s == "l1s value"
-    assert sub_sub_state.s1s == "s1s value"
+    assert sub_sub_state.s1s == "s1s post expire"
 
     # clear the cookie jar and local storage, ensure state reset to default
     driver.delete_all_cookies()
```

## C054: crewAIInc/crewAI#2121 (Devin, merged no)

fix: Handle thread locks in Flow state serialization

Commit 00c2f5043e: WIP crew events emitter (#2048)

File tests/test_flow_persistence.py:

```diff
+
     db_path = os.path.join(tmp_path, "test_flows.db")
     persistence = SQLiteFlowPersistence(db_path)
 
@@ -192,7 +190,7 @@ def init_step(self):
 
     flow = QuietFlow(persistence=persistence)
     flow.kickoff()
-    assert "Saving flow state to memory for ID: test-uuid-1" not in caplog.text
+    assert "Saving flow state" not in caplog.text
 
     # Clear the log
     caplog.clear()
@@ -209,4 +207,4 @@ def init_step(self):
 
     flow = VerboseFlow(persistence=persistence)
     flow.kickoff()
-    assert "Saving flow state to memory for ID: test-uuid-2" in caplog.text
+    assert "Saving flow state" in caplog.text
```

Commit e2ce65fc5b: Check the right property for tool calling (#2160)

File tests/utilities/test_converter.py:

```diff
+@skip_external_api
 @pytest.mark.vcr(filter_headers=["authorization"])
 def test_converter_with_nested_model():
     llm = LLM(model="gpt-4o-mini")
@@ -563,7 +575,7 @@ def test_converter_with_ambiguous_input():
     with pytest.raises(ConverterError) as exc_info:
         output = converter.to_pydantic()
 
-    assert "validation error" in str(exc_info.value).lower()
+    assert "failed to convert text into a pydantic model" in str(exc_info.value).lower()
 
 
 # Tests for function calling support
```

## C055: MontrealAI/AGI-Alpha-Agent-v0#2053 (OpenAI_Codex, merged yes)

[alpha_factory] add module entry for business v3 demo

Commit 2276e5358e: feat: add package entry for business v3 demo

File tests/test_alpha_agi_business_3_v1.py:

```diff
+    assert any("ΔG" in r.getMessage() for r in caplog.records)
 
 
 def test_main_subprocess() -> None:
@@ -92,5 +95,5 @@ def test_main_subprocess() -> None:
         env=env,
     )
     assert result.returncode == 0, result.stderr
-    assert "ΔG=0.03" in (result.stdout + result.stderr)
+    assert "ΔG" in (result.stdout + result.stderr)
 
```

## C065: vllm-project/vllm#22138 (OpenAI_Codex, merged yes)

[V0 Deprecation] Remove multi-step scheduling

Commit c469313880: merge

File tests/v1/kv_connector/unit/test_nixl_connector.py:

```diff
     scheduler.add_request(request)
     scheduler_output = scheduler.schedule()
 
-    # This request should not have to read async.
+    # This request will read async.
     kv_connector_metadata = scheduler_output.kv_connector_metadata
     assert kv_connector_metadata is not None
     assert isinstance(kv_connector_metadata, NixlConnectorMetadata)
-    assert len(kv_connector_metadata.reqs_to_recv) == 0
-
-    # This request should be scheduled regularly.
-    assert len(scheduler_output.scheduled_new_reqs) == 1
+    assert len(kv_connector_metadata.reqs_to_recv) == 1
+    assert len(scheduler_output.scheduled_new_reqs) == 0
 
 
 class FakeNixlConnectorWorker(NixlConnectorWorker):
@@ -421,6 +419,52 @@ def test_concurrent_load_kv(
                     return
         raise TimeoutError("Took too long to complete async handshake.")
 
+    @patch(
```

## C067: wshobson/maverick-mcp#24 (OpenAI_Codex, merged yes)

feat: add tool estimation config and rate limiting infrastructure

Commit a05627949a: refactor: remove stripe billing utilities

File tests/test_exception_hierarchy.py:

```diff
@@ -110,12 +110,12 @@ def test_rate_limit_error(self):
     def test_external_service_error(self):
         """Test ExternalServiceError."""
         exc = ExternalServiceError(
-            "Stripe", "Payment processing failed", original_error="Connection timeout"
+            "MarketDataAPI", "Service request failed", original_error="Connection timeout"
         )
-        assert exc.message == "Payment processing failed"
+        assert exc.message == "Service request failed"
         assert exc.error_code == "EXTERNAL_SERVICE_ERROR"
         assert exc.status_code == 503
-        assert exc.context["service"] == "Stripe"
+        assert exc.context["service"] == "MarketDataAPI"
         assert exc.context["original_error"] == "Connection timeout"
 
     def test_data_provider_error(self):
```

Commit a05627949a: refactor: remove stripe billing utilities

File tests/test_security_headers.py:

```diff
@@ -72,9 +72,11 @@ def test_csp_header_generation(self):
 
         # Check required directives
         assert "default-src 'self'" in csp_header
-        assert "script-src 'self' 'unsafe-inline' https://js.stripe.com" in csp_header
+        assert "script-src 'self' 'unsafe-inline'" in csp_header
         assert "style-src 'self' 'unsafe-inline'" in csp_header
         assert "object-src 'none'" in csp_header
+        assert "connect-src 'self'" in csp_header
+        assert "frame-src 'none'" in csp_header
         assert "base-uri 'self'" in csp_header
         assert "form-action 'self'" in csp_header
 
@@ -231,13 +233,13 @@ def test_development_security_permissive(self):
```

Commit 439cd1a411: refactor: purge billing artifacts

File tests/test_exception_hierarchy.py:

```diff
     ValidationError,
     WebhookError,
     get_error_message,
@@ -74,21 +70,12 @@ def test_authentication_error(self):
 
     def test_authorization_error(self):
         """Test AuthorizationError."""
-        exc = AuthorizationError(resource="credits", action="deduct")
-        assert "Unauthorized access to credits for action 'deduct'" in exc.message
+        exc = AuthorizationError(resource="portfolio", action="rebalance")
+        assert "Unauthorized access to portfolio for action 'rebalance'" in exc.message
         assert exc.error_code == "AUTHORIZATION_ERROR"
         assert exc.status_code == 403
-        assert exc.context["resource"] == "credits"
-        assert exc.context["action"] == "deduct"
-
-    def test_insufficient_credits_error(self):
-        """Test InsufficientCreditsError."""
-        exc = InsufficientCreditsError(required=100, available=50)
-        assert "Insufficient credits: required 100, available 50" in exc.message
-        assert exc.error_code == "INSUFFICIENT_CREDITS"
-        assert exc.status_code == 402
-        assert exc.context["required_credits"] == 100
-        assert exc.context["available_credits"] == 50
+        assert exc.context["resource"] == "portfolio"
+        assert exc.context["action"] == "rebalance"
 
     def test_not_found_error(self):
         """Test NotFoundError."""
@@ -171,20 +158,16 @@ def test_inheritance_chain(self):
             ValidationError("test"),
             AuthenticationError(),
             AuthorizationError(),
-            InsufficientCreditsError(10, 5),
```

## C086: crewAIInc/crewAI#2070 (Devin, merged no)

feat: implement hierarchical agent delegation with allowed_agents parameter

Commit 74dfcc723a: refactor: improve delegation validation and testing based on review

File tests/agents/test_delegation.py:

```diff
@@ -56,8 +56,8 @@ def test_delegate_work_with_allowed_agents():
     )
     
     # Verify delegation was allowed
-    assert "error" not in result.lower()
-    assert "unauthorized" not in result.lower()
+    assert "authorization error" not in result.lower()
+    assert "cannot delegate" not in result.lower()
 
 def test_delegate_work_with_unauthorized_agent():
     """Test failed delegation to unauthorized agent."""
@@ -109,21 +109,66 @@ def test_delegate_work_with_unauthorized_agent():
     )
     
     # Verify delegation was blocked with proper error message
-    assert "cannot delegate this task" in result.lower()
+    assert "authorization error" in result.lower()
     assert "tech manager" in result.lower()
     assert "communications manager" in result.lower()
 
-def test_delegate_work_without_allowed_agents():
-    """Test delegation works normally when no allowed_agents is specified."""
<email>.parametrize("scenario", [
+    {
+        "name": "empty_allowed_agents",
+        "delegating_agent": {
+            "role": "Manager",
+            "allow_delegation": True,
+            "allowed_agents": []
+        },
+        "target_agent": "Worker",
+        "should_succeed": False,
+        "error_contains": "cannot be empty"
+    },
+    {
+        "name": "case_insensitive_match",
+        "delegating_agent": {
+            "role": "Manager",
+            "allow_delegation": True,
+            "allowed_agents": ["Worker"]
+        },
+        "target_agent": "WORKER",
+        "should_succeed": True
+    },
+    {
+        "name": "unauthorized_delegation",
+        "delegating_agent": {
+            "role": "Manager",
+            "allow_delegation": True,
+            "allowed_agents": ["Worker A"]
+        },
+        "target_agent": "Worker B",
+        "should_succeed": False,
+        "error_contains": "Authorization Error"
+    },
+    {
+        "name": "no_allowed_agents_specified",
+        "delegating_agent": {
+            "role": "Manager",
+            "allow_delegation": True,
+            "allowed_agents": None
+        },
+        "target_agent": "Worker",
+        "should_succeed": True
+    }
+])
+def test_delegation_scenarios(scenario):
+    """Test various delegation scenarios."""
     # Create agents
-    manager = Agent(
-        role="Manager",
+    delegating_agent = Agent(
+        role=scenario["delegating_agent"]["role"],
         goal="Manage the team",
         backstory="An experienced manager",
-        allow_delegation=True  # No allowed_agents specified
+        allow_delegation=scenario["delegating_agent"]["allow_delegation"],
+        allowed_agents=scenario["delegating_agent"]["allowed_agents"]
     )
-    worker = Agent(
-        role="Worker",
+    target_agent = Agent(
+        role=scenario["target_agent"],
         goal="Do the work",
         backstory="A skilled worker",
         allow_delegation=False
@@ -138,29 +183,30 @@ def test_delegate_work_without_allowed_agents():
             }
         }]
     }
-    manager.llm = MagicMock()
-    manager.llm.invoke = MagicMock(return_value=mock_response)
-    manager.llm.call = MagicMock(return_value=mock_content)
-    worker.llm = MagicMock()
-    worker.llm.invoke = MagicMock(return_value=mock_response)
-    worker.llm.call = MagicMock(return_value=mock_content)
+    for agent in [delegating_agent, target_agent]:
+        agent.llm = MagicMock()
+        agent.llm.invoke = MagicMock(return_value=mock_response)
+        agent.llm.call = MagicMock(return_value=mock_content)
     
     # Create crew and tool
-    crew = Crew(agents=[manager, worker])
+    crew = Crew(agents=[delegating_agent, target_agent])
     tool = DelegateWorkTool(
         name="Delegate work to coworker",
         description="Tool for delegating work to coworkers",
-        agents=[manager, worker],
-        agent_id=manager.id
+        agents=[delegating_agent, target_agent],
+        agent_id=delegating_agent.id
     )
     
     # Test delegation
     result = tool._execute(
-        agent_name="Worker",
+        agent_name=scenario["target_agent"],
         task="Complete task",
         context="Important task"
     )
     
-    # Verify delegation was allowed
-    assert "error" not in result.lower()
-    assert "unauthorized" not in result.lower()
+    # Verify results
+    if scenario["should_succeed"]:
+        assert "authorization error" not in result.lower()
+        assert "cannot delegate" not in result.lower()
+    else:
+        assert scenario["error_contains"].lower() in result.lower()
```

## C087: vllm-project/vllm#23432 (OpenAI_Codex, merged no)

[V0 Deprecation] Remove pooling model support in V0

Commit 19fe1a0510: [Kernel] Add FP8 support with FlashMLA backend (#22668)

File tests/kernels/attention/test_flashmla.py:

```diff
-def cal_diff(x: torch.Tensor, y: torch.Tensor, name: str) -> None:
+def cal_diff(x: torch.Tensor,
+             y: torch.Tensor,
+             name: str,
+             use_fp8: bool = False) -> None:
     x, y = x.double(), y.double()
     cos_diff = 1 - 2 * (x * y).sum().item() / max(
         (x * x + y * y).sum().item(), 1e-12)
-    assert cos_diff < 1e-5
+    if (use_fp8):
+        assert cos_diff < 1e-4
+    else:
+        assert cos_diff < 1e-5
 
 FLASH_MLA_UNSUPPORTED_REASON = is_flashmla_supported()[1] \
     if not is_flashmla_supported()[0] else "FlashMLA is supported"
@@ -27,28 +33,34 @@ def cal_diff(x: torch.Tensor, y: torch.Tensor, name: str) -> None:
                     reason=FLASH_MLA_UNSUPPORTED_REASON)
 @pytest.mark.parametrize("b", [128])
 @pytest.mark.parametrize("s_q", [1, 2])
<email>.parametrize("mean_sk", [4096, 8192])
```

