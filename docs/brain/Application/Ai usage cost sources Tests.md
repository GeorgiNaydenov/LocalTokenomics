---
title: Ai usage cost sources Tests
aliases: []
tags: [tests]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
verified-against: 4d81cedd5403
chunk: ch-localtokenomics-src-ai-usage-cost-sources
approved-by: human
approved-at: '2026-11-19T00:12:14+00:00'
---

# Ai usage cost sources Tests

The tests that cover the Ai usage cost sources chunk and what they check.

## How it works

515 tests exercise this chunk. 0 of its 22 files are not imported by any test.

## Reference

%% generated:chunk-tests start (do not edit; run brain docs generate) %%
| Test | Scenario | File | Code |
|---|---|---|---|
| `test_only_planner_response_records_become_events` | Only planner response records become events | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:19` |
| `test_model_carries_forward_from_settings_change_text` | Model carries forward from settings change text | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:25` |
| `test_cwd_carries_forward_to_the_next_planner_response` | Cwd carries forward to the next planner response | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:32` |
| `test_session_id_comes_from_the_brain_directory_name` | Session id comes from the brain directory name | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:39` |
| `test_tokens_are_always_none` | Tokens are always none | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:45` |
| `test_a_session_with_no_model_selection_message_stays_unavailable_not_broken` | A session with no model selection message stays unavailable not broken | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:50` |
| `test_transcript_full_is_preferred_over_transcript` | Transcript full is preferred over transcript | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:67` |
| `test_real_fixture_prefers_transcript_full` | Real fixture prefers transcript full | `tests/test_antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:92` |
| `test_meta_describes_the_scan` | Meta describes the scan | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:77` |
| `test_meta_last_seen_reflects_the_full_scan_not_a_report_filter` | Meta last seen reflects the full scan not a report filter | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:121` |
| `test_report_returns_the_expected_shape` | Report returns the expected shape | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:133` |
| `test_session_title_serializes_with_the_folder_fallback` | Session title serializes with the folder fallback | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:189` |
| `test_computed_fields_are_serialized` | Computed fields are serialized | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:199` |
| `test_client_filter_narrows_the_report` | Client filter narrows the report | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:233` |
| `test_provider_filter_narrows_the_report` | Provider filter narrows the report | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:242` |
| `test_date_filter_narrows_the_report` | Date filter narrows the report | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:247` |
| `test_include_sidechains_false_drops_the_subagent_event` | Include sidechains false drops the subagent event | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:253` |
| `test_model_and_project_filters_compose` | Model and project filters compose | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:259` |
| `test_states_filter_narrows_the_report` | States filter narrows the report | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:267` |
| `test_search_filter_narrows_the_report` | Search filter narrows the report | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:276` |
| `test_a_filter_that_matches_nothing_returns_an_empty_report` | A filter that matches nothing returns an empty report | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:284` |
| `test_rates_returns_the_loaded_table` | Rates returns the loaded table | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:291` |
| `test_meta_and_report_carry_the_rates_age_and_model_matches` | Meta and report carry the rates age and model matches | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:314` |
| `test_sources_expose_the_experimental_flag` | Sources expose the experimental flag | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:326` |
| `test_cursor_is_registered_with_nothing_available` | Cursor is registered with nothing available | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:333` |
| `test_every_parent_id_resolves_inside_the_trace` | Every parent id resolves inside the trace | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:349` |
| `test_an_unknown_session_has_no_trace` | An unknown session has no trace | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:364` |
| `test_spans_are_loaded_once_and_shared_across_endpoints` | Spans are loaded once and shared across endpoints | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:368` |
| `test_refresh_invalidates_the_span_cache` | Refresh invalidates the span cache | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:392` |
| `test_deleting_a_session_invalidates_only_its_own_cache_entry` | Deleting a session invalidates only its own cache entry | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:427` |
| `test_economics_totals_equal_the_sum_over_model_calls` | Economics totals equal the sum over model calls | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:454` |
| `test_economics_reports_absent_tokens_rather_than_zero` | Economics reports absent tokens rather than zero | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:472` |
| `test_report_and_economics_agree_without_token_counts` | Report and economics agree without token counts | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:483` |
| `test_claude_code_context_capacity_is_estimated_from_the_rate_table` | Claude code context capacity is estimated from the rate table | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:497` |
| `test_codex_context_occupancy_is_derived_from_the_logged_window` | Codex context occupancy is derived from the logged window | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:512` |
| `test_an_outcome_round_trips_and_carries_computed_signals` | An outcome round trips and carries computed signals | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:525` |
| `test_deleting_a_session_removes_its_trace_but_not_its_requests` | Deleting a session removes its trace but not its requests | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:553` |
| `test_span_content_is_unavailable_while_metadata_only_is_on` | Span content is unavailable while metadata only is on | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:568` |
| `test_span_content_is_redacted_when_content_capture_is_allowed` | Span content is redacted when content capture is allowed | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:574` |
| `test_the_report_can_be_filtered_by_trace_data_and_errors` | The report can be filtered by trace data and errors | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:591` |
| `test_by_turn_rows_carry_ordinal_started_at_and_a_privacy_gated_label` | By turn rows carry ordinal started at and a privacy gated label | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:610` |
| `test_totals_report_how_many_events_actually_priced_the_dollar_figure` | Totals report how many events actually priced the dollar figure | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:630` |
| `test_files_in_slice_narrows_with_the_report_but_files_scanned_does_not` | Files in slice narrows with the report but files scanned does not | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:638` |
| `test_session_is_sidechain_only_when_every_event_is_but_has_sidechain_on_any` | Session is sidechain only when every event is but has sidechain on any | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:661` |
| `test_session_cost_state_is_the_worst_of_its_requests_with_mixed_states_kept` | Session cost state is the worst of its requests with mixed states kept | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:680` |
| `test_build_report_files_in_slice_counts_distinct_source_files_in_the_filtered_set` | Build report files in slice counts distinct source files in the filtered set | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:692` |
| `test_meta_warning_summary_counts_instances_by_severity` | Meta warning summary counts instances by severity | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:765` |
| `test_meta_session_warnings_keys_by_session_id_with_sorted_kinds` | Meta session warnings keys by session id with sorted kinds | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:778` |
| `test_meta_warning_summary_is_all_zero_when_nothing_is_flagged` | Meta warning summary is all zero when nothing is flagged | `tests/test_api.py` | [[tests/test_api.py]] `tests/test_api.py:788` |
| `test_four_token_buckets_map_straight_across` | Four token buckets map straight across | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:52` |
| `test_input_tokens_is_taken_as_already_excluding_cache` | Input tokens is taken as already excluding cache | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:61` |
| `test_cache_creation_supplies_the_5m_1h_split` | Cache creation supplies the 5m 1h split | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:69` |
| `test_missing_cache_creation_falls_back_to_the_5m_bucket` | Missing cache creation falls back to the 5m bucket | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:75` |
| `test_usage_iterations_are_not_summed_on_top_of_the_top_level_block` | Usage iterations are not summed on top of the top level block | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:83` |
| `test_thinking_tokens_are_recorded_but_not_billed` | Thinking tokens are recorded but not billed | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:93` |
| `test_synthetic_and_zero_token_records_are_skipped` | Synthetic and zero token records are skipped | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:102` |
| `test_non_assistant_records_are_ignored` | Non assistant records are ignored | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:109` |
| `test_repeated_message_id_and_request_id_in_one_file_yields_two_events` | Repeated message id and request id in one file yields two events | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:122` |
| `test_the_same_record_in_two_files_has_the_same_request_id` | The same record in two files has the same request id | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:128` |
| `test_is_sidechain_and_fast_speed_are_carried_through` | Is sidechain and fast speed are carried through | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:134` |
| `test_service_tier_batch_becomes_the_batch_tier` | Service tier batch becomes the batch tier | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:142` |
| `test_default_tier_is_standard` | Default tier is standard | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:148` |
| `test_project_name_comes_from_cwd` | Project name comes from cwd | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:152` |
| `test_custom_title_record_sets_the_title_and_tool_source` | Custom title record sets the title and tool source | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:163` |
| `test_a_later_custom_title_record_wins_over_an_earlier_one` | A later custom title record wins over an earlier one | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:177` |
| `test_no_custom_title_falls_back_to_the_folder_title` | No custom title falls back to the folder title | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:192` |
| `test_a_message_split_over_three_records_yields_three_parse_events` | A message split over three records yields three parse events | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:212` |
| `test_a_message_split_over_three_records_keeps_the_largest_output_in_the_trace` | A message split over three records keeps the largest output in the trace | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:218` |
| `test_session_id_and_timestamp_come_from_the_record` | Session id and timestamp come from the record | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:231` |
| `test_parse_resume_yields_only_records_after_the_offset` | Parse resume yields only records after the offset | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:242` |
| `test_parse_resume_carries_a_seeded_title_forward` | Parse resume carries a seeded title forward | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:265` |
| `test_parse_resume_picks_up_a_title_that_changes_after_the_offset` | Parse resume picks up a title that changes after the offset | `tests/test_claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:293` |
| `test_sources_registered_and_experimental` | Sources registered and experimental | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:59` |
| `test_cline_legacy_counted_records_and_skips` | Cline legacy counted records and skips | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:73` |
| `test_cline_legacy_tokens_exclusive_policy_and_cost` | Cline legacy tokens exclusive policy and cost | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:86` |
| `test_cancelled_request_without_cost_is_counted` | Cancelled request without cost is counted | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:106` |
| `test_deleted_api_reqs_and_subagent_usage_counted` | Deleted api reqs and subagent usage counted | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:113` |
| `test_model_falls_back_to_nearest_earlier_task_metadata_entry` | Model falls back to nearest earlier task metadata entry | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:123` |
| `test_request_text_never_leaks` | Request text never leaks | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:131` |
| `test_partial_entries_skipped` | Partial entries skipped | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:137` |
| `test_bad_json_text_and_missing_keys_do_not_crash` | Bad json text and missing keys do not crash | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:144` |
| `test_duplicate_task_and_timestamp_emitted_once` | Duplicate task and timestamp emitted once | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:161` |
| `test_truncated_array_is_salvaged_with_warning` | Truncated array is salvaged with warning | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:168` |
| `test_non_array_file_warns` | Non array file warns | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:177` |
| `test_missing_root_yields_nothing` | Missing root yields nothing | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:185` |
| `test_inclusive_policy_subtracts_cache_and_clamps` | Inclusive policy subtracts cache and clamps | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:193` |
| `test_exclusive_policy_keeps_tokens_in` | Exclusive policy keeps tokens in | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:204` |
| `test_policy_table_per_source` | Policy table per source | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:210` |
| `test_roo_inclusive_no_model_with_cost_and_subtask` | Roo inclusive no model with cost and subtask | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:221` |
| `test_kilo_legacy_source_and_policy` | Kilo legacy source and policy | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:240` |
| `test_lowercase_directory_names_matched` | Lowercase directory names matched | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:254` |
| `test_default_roots_linux_variants` | Default roots linux variants | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:268` |
| `test_sdk_root_env_overrides` | Sdk root env overrides | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:284` |
| `test_files_finds_task_and_sdk_files` | Files finds task and sdk files | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:295` |
| `test_sdk_messages_inclusive_with_manifest_fallbacks` | Sdk messages inclusive with manifest fallbacks | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:307` |
| `test_sdk_legacy_migrated_session_skipped_and_subagent_flagged` | Sdk legacy migrated session skipped and subagent flagged | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:327` |
| `test_sdk_bad_file_warns` | Sdk bad file warns | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:335` |
| `test_reparse_is_idempotent_through_the_store` | Reparse is idempotent through the store | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:347` |
| `test_pipeline_prices_known_model_and_tolerates_unpriced` | Pipeline prices known model and tolerates unpriced | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:359` |
| `test_negative_token_fields_are_clamped` | Negative token fields are clamped | `tests/test_cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:377` |
| `test_cached_input_is_a_subset_of_input_tokens` | Cached input is a subset of input tokens | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:85` |
| `test_uncached_input_is_the_whole_input_when_nothing_was_cached` | Uncached input is the whole input when nothing was cached | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:92` |
| `test_reasoning_output_is_a_subset_of_output_and_not_double_counted` | Reasoning output is a subset of output and not double counted | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:101` |
| `test_cached_input_greater_than_input_is_clamped` | Cached input greater than input is clamped | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:110` |
| `test_model_comes_from_session_meta` | Model comes from session meta | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:117` |
| `test_mid_session_model_change_applies_only_to_later_events` | Mid session model change applies only to later events | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:121` |
| `test_session_id_and_project_come_from_session_meta` | Session id and project come from session meta | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:132` |
| `test_model_is_none_when_the_rollout_never_names_one` | Model is none when the rollout never names one | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:138` |
| `test_events_before_the_first_model_record_are_backfilled` | Events before the first model record are backfilled | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:143` |
| `test_all_zero_last_token_usage_events_are_skipped` | All zero last token usage events are skipped | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:167` |
| `test_records_without_last_token_usage_are_skipped` | Records without last token usage are skipped | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:172` |
| `test_token_count_at_the_top_level_is_still_parsed` | Token count at the top level is still parsed | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:187` |
| `test_top_level_envelope_alone_parses` | Top level envelope alone parses | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:194` |
| `test_originator_maps_to_the_codex_desktop_client` | Originator maps to the codex desktop client | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:223` |
| `test_unknown_originator_is_slugified_not_dropped` | Unknown originator is slugified not dropped | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:248` |
| `test_subagent_source_marks_is_sidechain` | Subagent source marks is sidechain | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:263` |
| `test_no_session_meta_still_parses_with_default_client` | No session meta still parses with default client | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:278` |
| `test_matching_session_total_produces_no_warning` | Matching session total produces no warning | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:285` |
| `test_disagreeing_session_total_warns_and_names_the_file` | Disagreeing session total warns and names the file | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:291` |
| `test_a_real_total_with_an_all_zero_breakdown_still_counts_toward_reconciliation` | A real total with an all zero breakdown still counts toward reconciliation | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:301` |
| `test_drift_within_tolerance_is_not_warned_about` | Drift within tolerance is not warned about | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:323` |
| `test_large_absolute_drift_under_one_percent_is_not_warned_about` | Large absolute drift under one percent is not warned about | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:335` |
| `test_duplicate_token_count_events_with_an_unchanged_total_are_not_double_counted` | Duplicate token count events with an unchanged total are not double counted | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:342` |
| `test_token_usage_record_is_parsed_and_preferred_exclusively_over_token_count` | Token usage record is parsed and preferred exclusively over token count | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:361` |
| `test_a_file_without_token_usage_records_still_uses_token_count` | A file without token usage records still uses token count | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:391` |
| `test_forked_thread_reconciliation_subtracts_inherited_history` | Forked thread reconciliation subtracts inherited history | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:396` |
| `test_the_same_shape_without_forked_from_id_still_warns` | The same shape without forked from id still warns | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:422` |
| `test_a_counter_reset_gets_its_own_warning_kind_not_a_drift_percentage` | A counter reset gets its own warning kind not a drift percentage | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:442` |
| `test_thread_name_from_session_index_sets_the_tool_title` | Thread name from session index sets the tool title | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:472` |
| `test_a_command_name_wrapper_thread_name_falls_through_to_folder` | A command name wrapper thread name falls through to folder | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:502` |
| `test_no_session_index_file_falls_back_to_folder_title` | No session index file falls back to folder title | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:534` |
| `test_session_index_is_shared_across_every_rollout_file_under_one_root` | Session index is shared across every rollout file under one root | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:540` |
| `test_fingerprint_disambiguates_duplicate_token_count_fallback_keys` | Fingerprint disambiguates duplicate token count fallback keys | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:588` |
| `test_service_tier_maps_to_a_price_tier` | Service tier maps to a price tier | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:648` |
| `test_a_rollout_that_never_names_a_tier_is_standard_and_keeps_its_models` | A rollout that never names a tier is standard and keeps its models | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:653` |
| `test_a_late_tier_is_not_applied_to_events_that_ran_before_it` | A late tier is not applied to events that ran before it | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:674` |
| `test_only_the_model_is_backfilled_the_tier_is_the_one_in_force_at_the_time` | Only the model is backfilled the tier is the one in force at the time | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:688` |
| `test_a_tier_change_mid_session_applies_only_to_later_events` | A tier change mid session applies only to later events | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:710` |
| `test_a_settings_record_without_a_tier_resets_to_standard` | A settings record without a tier resets to standard | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:723` |
| `test_a_non_settings_record_without_a_tier_does_not_reset_it` | A non settings record without a tier does not reset it | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:734` |
| `test_parsing_a_large_rollout_with_no_tier_stays_linear` | Parsing a large rollout with no tier stays linear | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:748` |
| `test_the_tier_also_applies_to_token_usage_record_files` | The tier also applies to token usage record files | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:769` |
| `test_the_tier_fixture_carries_the_real_key_path` | The tier fixture carries the real key path | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:774` |
| `test_a_priority_event_is_priced_at_the_priority_variant` | A priority event is priced at the priority variant | `tests/test_codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:779` |
| `test_each_turn_yields_one_event` | Each turn yields one event | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:28` |
| `test_populated_session_carries_cwd_repository_branch_and_project` | Populated session carries cwd repository branch and project | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:32` |
| `test_second_turn_in_same_session_gets_its_own_request_id` | Second turn in same session gets its own request id | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:48` |
| `test_null_cwd_falls_back_to_no_project` | Null cwd falls back to no project | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:56` |
| `test_session_summary_becomes_the_tool_title` | Session summary becomes the tool title | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:64` |
| `test_null_summary_falls_back_to_the_folder_title` | Null summary falls back to the folder title | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:70` |
| `test_empty_database_yields_no_events_and_no_warnings` | Empty database yields no events and no warnings | `tests/test_copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:76` |
| `test_basic_fixture_maps_tokens_and_metadata` | Basic fixture maps tokens and metadata | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:77` |
| `test_title_comes_from_workspace_yaml_name` | Title comes from workspace yaml name | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:102` |
| `test_title_falls_back_to_summary_then_folder` | Title falls back to summary then folder | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:107` |
| `test_workspace_yaml_supplies_cwd_when_start_has_no_context` | Workspace yaml supplies cwd when start has no context | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:119` |
| `test_ephemeral_usage_events_are_ignored` | Ephemeral usage events are ignored | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:131` |
| `test_ephemeral_shutdown_is_skipped` | Ephemeral shutdown is skipped | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:137` |
| `test_resume_emits_deltas_between_cumulative_shutdowns` | Resume emits deltas between cumulative shutdowns | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:144` |
| `test_deltas_are_tracked_per_model` | Deltas are tracked per model | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:166` |
| `test_smaller_total_is_a_counter_reset_and_taken_whole` | Smaller total is a counter reset and taken whole | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:180` |
| `test_crashed_session_without_shutdown_warns_and_emits_nothing` | Crashed session without shutdown warns and emits nothing | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:195` |
| `test_output_after_last_shutdown_warns_but_keeps_earlier_events` | Output after last shutdown warns but keeps earlier events | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:208` |
| `test_idle_session_without_shutdown_does_not_warn` | Idle session without shutdown does not warn | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:223` |
| `test_compaction_complete_is_its_own_event_when_enabled` | Compaction complete is its own event when enabled | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:229` |
| `test_agent_metrics_are_not_double_counted` | Agent metrics are not double counted | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:263` |
| `test_copilot_credits_in_raw_and_no_reported_cost` | Copilot credits in raw and no reported cost | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:269` |
| `test_dotted_model_passes_through_and_prices_via_matcher` | Dotted model passes through and prices via matcher | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:275` |
| `test_negative_and_odd_values_never_go_negative` | Negative and odd values never go negative | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:283` |
| `test_malformed_lines_and_missing_keys_do_not_crash` | Malformed lines and missing keys do not crash | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:292` |
| `test_missing_root_yields_nothing` | Missing root yields nothing | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:310` |
| `test_copilot_home_env_override` | Copilot home env override | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:315` |
| `test_reparse_is_idempotent_and_fingerprints_are_unique` | Reparse is idempotent and fingerprints are unique | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:322` |
| `test_source_is_experimental_and_discovered` | Source is experimental and discovered | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:337` |
| `test_end_to_end_pipeline_prices_known_and_tolerates_unknown_model` | End to end pipeline prices known and tolerates unknown model | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:343` |
| `test_compaction_is_not_counted_by_default` | Compaction is not counted by default | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:372` |
| `test_negative_inputs_are_clamped_to_zero` | Negative inputs are clamped to zero | `tests/test_copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:386` |
| `test_each_composer_yields_one_event` | Each composer yields one event | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:28` |
| `test_composer_id_and_timestamp_come_from_the_row` | Composer id and timestamp come from the row | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:32` |
| `test_second_composer_gets_its_own_request_id` | Second composer gets its own request id | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:42` |
| `test_composer_name_becomes_the_tool_title` | Composer name becomes the tool title | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:48` |
| `test_missing_name_falls_back_to_the_folder_title` | Missing name falls back to the folder title | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:58` |
| `test_empty_database_yields_no_events_and_no_warnings` | Empty database yields no events and no warnings | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:73` |
| `test_missing_cursor_disk_kv_table_yields_no_events_and_no_warnings` | Missing cursor disk kv table yields no events and no warnings | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:80` |
| `test_missing_file_yields_no_events_and_no_warnings` | Missing file yields no events and no warnings | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:87` |
| `test_discovers_global_and_workspace_state_dbs` | Discovers global and workspace state dbs | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:93` |
| `test_no_installation_yields_no_files` | No installation yields no files | `tests/test_cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:108` |
| `test_demo_store_is_separate_from_the_real_store` | Demo store is separate from the real store | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:27` |
| `test_every_source_is_pointed_inside_the_demo_tree` | Every source is pointed inside the demo tree | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:33` |
| `test_generate_twice_converges` | Generate twice converges | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:40` |
| `test_demo_analysis_reads_only_generated_files` | Demo analysis reads only generated files | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:47` |
| `test_off_removes_the_demo_tree_then_serves_real_data` | Off removes the demo tree then serves real data | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:61` |
| `test_demo_shows_priced_estimated_and_unpriced_states` | Demo shows priced estimated and unpriced states | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:89` |
| `test_demo_context_windows_come_from_the_rate_table` | Demo context windows come from the rate table | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:111` |
| `test_demo_is_deterministic` | Demo is deterministic | `tests/test_demo.py` | [[tests/test_demo.py]] `tests/test_demo.py:117` |
| `test_only_assistant_rows_produce_events` | Only assistant rows produce events | `tests/test_dyad.py` | [[tests/test_dyad.py]] `tests/test_dyad.py:28` |
| `test_repo_populated_app_maps_org_and_repo` | Repo populated app maps org and repo | `tests/test_dyad.py` | [[tests/test_dyad.py]] `tests/test_dyad.py:32` |
| `test_repo_missing_app_maps_repository_to_none` | Repo missing app maps repository to none | `tests/test_dyad.py` | [[tests/test_dyad.py]] `tests/test_dyad.py:45` |
| `test_chat_title_becomes_the_tool_title` | Chat title becomes the tool title | `tests/test_dyad.py` | [[tests/test_dyad.py]] `tests/test_dyad.py:56` |
| `test_null_chat_title_falls_back_to_the_folder_title` | Null chat title falls back to the folder title | `tests/test_dyad.py` | [[tests/test_dyad.py]] `tests/test_dyad.py:66` |
| `test_basic_fixture_totals_and_metadata` | Basic fixture totals and metadata | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:57` |
| `test_subagent_file_is_sidechain` | Subagent file is sidechain | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:81` |
| `test_tool_added_only_when_total_reconciles` | Tool added only when total reconciles | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:87` |
| `test_inclusive_cached_never_negative` | Inclusive cached never negative | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:95` |
| `test_null_tokens_skipped_and_missing_keys_tolerated` | Null tokens skipped and missing keys tolerated | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:101` |
| `test_title_falls_back_to_folder_and_session_to_filename` | Title falls back to folder and session to filename | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:110` |
| `test_project_root_marker` | Project root marker | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:117` |
| `test_set_messages_checkpoint_and_last_summary_wins` | Set messages checkpoint and last summary wins | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:126` |
| `test_malformed_and_truncated_lines_warn` | Malformed and truncated lines warn | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:140` |
| `test_legacy_whole_file_json` | Legacy whole file json | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:148` |
| `test_files_ignore_unrelated_antigravity_data` | Files ignore unrelated antigravity data | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:161` |
| `test_env_override` | Env override | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:172` |
| `test_reparse_is_idempotent_through_the_store` | Reparse is idempotent through the store | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:177` |
| `test_source_is_experimental_and_discovered` | Source is experimental and discovered | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:185` |
| `test_pipeline_prices_known_model_and_survives_unknown` | Pipeline prices known model and survives unknown | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:190` |
| `test_negative_token_fields_clamp_to_zero` | Negative token fields clamp to zero | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:207` |
| `test_id_less_identical_lines_dedup` | Id less identical lines dedup | `tests/test_gemini_cli.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:214` |
| `test_basic_fixture_yields_only_turn_completed_events_with_nonzero_tokens` | Basic fixture yields only turn completed events with nonzero tokens | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:59` |
| `test_cached_input_is_split_out_of_input_tokens` | Cached input is split out of input tokens | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:68` |
| `test_top_level_usage_is_used_when_model_usage_map_is_absent` | Top level usage is used when model usage map is absent | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:76` |
| `test_cache_creation_tokens_become_cache_write_and_are_not_double_counted` | Cache creation tokens become cache write and are not double counted | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:83` |
| `test_session_and_project_come_from_summary_json` | Session and project come from summary json | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:93` |
| `test_session_and_project_fall_back_to_url_decoded_directory_names` | Session and project fall back to url decoded directory names | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:100` |
| `test_non_turn_completed_updates_are_skipped` | Non turn completed updates are skipped | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:110` |
| `test_turn_completed_without_usage_is_skipped` | Turn completed without usage is skipped | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:119` |
| `test_all_zero_token_turns_are_skipped` | All zero token turns are skipped | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:133` |
| `test_multiple_models_in_one_turn_emit_one_event_each` | Multiple models in one turn emit one event each | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:139` |
| `test_request_id_includes_event_id_and_model_for_dedup` | Request id includes event id and model for dedup | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:163` |
| `test_model_is_unknown_without_summary_or_model_usage_map` | Model is unknown without summary or model usage map | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:170` |
| `test_agent_timestamp_ms_takes_priority_over_envelope_seconds` | Agent timestamp ms takes priority over envelope seconds | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:176` |
| `test_envelope_seconds_are_used_when_agent_timestamp_is_absent` | Envelope seconds are used when agent timestamp is absent | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:184` |
| `test_line_session_id_wins_over_summary_id` | Line session id wins over summary id | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:192` |
| `test_summary_session_id_is_used_when_line_omits_it` | Summary session id is used when line omits it | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:202` |
| `test_default_roots_uses_grok_home_when_set` | Default roots uses grok home when set | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:212` |
| `test_default_roots_falls_back_to_home_dot_grok` | Default roots falls back to home dot grok | `tests/test_grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:219` |
| `test_a_single_hit_keeps_its_own_sentence` | A single hit keeps its own sentence | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:57` |
| `test_many_hits_of_the_same_kind_collapse_into_one_insight` | Many hits of the same kind collapse into one insight | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:67` |
| `test_no_em_dash_in_any_generated_message` | No em dash in any generated message | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:81` |
| `test_a_quiet_session_has_no_amplification_insight` | A quiet session has no amplification insight | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:89` |
| `test_cache_miss_worst_pick_is_the_lowest_ratio_not_the_highest` | Cache miss worst pick is the lowest ratio not the highest | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:95` |
| `test_amplification_insight_uses_paid_tokens_not_cached_reads` | Amplification insight uses paid tokens not cached reads | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:130` |
| `test_the_shipped_claude_code_trace_fixture_produces_no_amplification_insight` | The shipped claude code trace fixture produces no amplification insight | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:160` |
| `test_context_pressure_fires_from_the_rate_table_capacity` | Context pressure fires from the rate table capacity | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:172` |
| `test_a_contributor_from_an_earlier_turn_is_not_lost_across_an_intervening_call` | A contributor from an earlier turn is not lost across an intervening call | `tests/test_insights.py` | [[tests/test_insights.py]] `tests/test_insights.py:201` |
| `test_only_assistant_messages_become_events` | Only assistant messages become events | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:19` |
| `test_client_and_provider_and_model_come_from_thread_json` | Client and provider and model come from thread json | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:24` |
| `test_tokens_are_none` | Tokens are none | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:33` |
| `test_session_id_matches_thread_id` | Session id matches thread id | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:38` |
| `test_missing_thread_json_yields_events_with_no_model` | Missing thread json yields events with no model | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:43` |
| `test_thread_json_title_becomes_the_tool_title` | Thread json title becomes the tool title | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:58` |
| `test_missing_thread_json_falls_back_to_the_folder_title` | Missing thread json falls back to the folder title | `tests/test_jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:64` |
| `test_kilo_events_use_kilo_source_and_same_mapping` | Kilo events use kilo source and same mapping | `tests/test_kilo_code.py` | [[tests/test_kilo_code.py]] `tests/test_kilo_code.py:28` |
| `test_kilo_roots_and_env` | Kilo roots and env | `tests/test_kilo_code.py` | [[tests/test_kilo_code.py]] `tests/test_kilo_code.py:43` |
| `test_kilo_finds_channel_dbs_not_opencode_dbs` | Kilo finds channel dbs not opencode dbs | `tests/test_kilo_code.py` | [[tests/test_kilo_code.py]] `tests/test_kilo_code.py:51` |
| `test_kilo_registered_experimental_and_missing_root_safe` | Kilo registered experimental and missing root safe | `tests/test_kilo_code.py` | [[tests/test_kilo_code.py]] `tests/test_kilo_code.py:57` |
| `test_basic_fixture_counts_each_step_once` | Basic fixture counts each step once | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:92` |
| `test_token_mapping_and_metadata` | Token mapping and metadata | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:100` |
| `test_cache_write_is_inside_input_by_default` | Cache write is inside input by default | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:119` |
| `test_cache_write_policy_constant_both_values` | Cache write policy constant both values | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:127` |
| `test_uncached_input_never_negative` | Uncached input never negative | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:142` |
| `test_cached_tokens_alias_used_when_cache_read_absent` | Cached tokens alias used when cache read absent | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:156` |
| `test_conflicting_cache_aliases_prefer_cache_read_and_warn` | Conflicting cache aliases prefer cache read and warn | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:165` |
| `test_trap_goal_usage_attribution_is_not_usage` | Trap goal usage attribution is not usage | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:177` |
| `test_trap_mirrored_child_stream_in_parent_is_skipped` | Trap mirrored child stream in parent is skipped | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:184` |
| `test_trap_replayed_prefix_dedups_on_stream_seq_and_usage_id` | Trap replayed prefix dedups on stream seq and usage id | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:196` |
| `test_replay_in_a_second_file_gets_the_same_request_id` | Replay in a second file gets the same request id | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:205` |
| `test_recorded_at_is_microseconds` | Recorded at is microseconds | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:216` |
| `test_timestamp_units_all_resolve_to_same_instant` | Timestamp units all resolve to same instant | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:224` |
| `test_retained_frame_wrapper_is_unwrapped` | Retained frame wrapper is unwrapped | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:230` |
| `test_unknown_shapes_are_skipped_with_one_aggregate_warning` | Unknown shapes are skipped with one aggregate warning | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:246` |
| `test_malformed_lines_and_missing_keys_do_not_crash` | Malformed lines and missing keys do not crash | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:261` |
| `test_missing_model_with_tokens_is_kept_unpriced` | Missing model with tokens is kept unpriced | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:275` |
| `test_echo_provider_produces_no_events` | Echo provider produces no events | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:281` |
| `test_session_without_stream_ids_or_seq_still_counts` | Session without stream ids or seq still counts | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:286` |
| `test_file_discovery_skips_view_and_catalog_dirs` | File discovery skips view and catalog dirs | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:292` |
| `test_missing_root_yields_nothing` | Missing root yields nothing | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:304` |
| `test_muse_data_dir_override` | Muse data dir override | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:309` |
| `test_xdg_and_home_default_roots` | Xdg and home default roots | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:315` |
| `test_source_is_experimental_and_discovered` | Source is experimental and discovered | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:323` |
| `test_reparse_is_idempotent_by_fingerprint` | Reparse is idempotent by fingerprint | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:329` |
| `test_pipeline_prices_events_and_survives_unknown_model` | Pipeline prices events and survives unknown model | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:336` |
| `test_negative_token_fields_clamp_to_zero` | Negative token fields clamp to zero | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:369` |
| `test_own_stream_fallback_survives_mirrored_child_first` | Own stream fallback survives mirrored child first | `tests/test_muse_code.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:388` |
| `test_only_assistant_rows_produce_events` | Only assistant rows produce events | `tests/test_ollama_app.py` | [[tests/test_ollama_app.py]] `tests/test_ollama_app.py:28` |
| `test_local_model_resolves_to_local_provider` | Local model resolves to local provider | `tests/test_ollama_app.py` | [[tests/test_ollama_app.py]] `tests/test_ollama_app.py:32` |
| `test_cloud_model_resolves_to_ollama_provider` | Cloud model resolves to ollama provider | `tests/test_ollama_app.py` | [[tests/test_ollama_app.py]] `tests/test_ollama_app.py:42` |
| `test_default_roots_is_empty` | Default roots is empty | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:22` |
| `test_cached_tokens_are_a_subset_of_prompt_tokens` | Cached tokens are a subset of prompt tokens | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:26` |
| `test_reasoning_tokens_are_a_subset_of_completion_tokens_and_output_stays_full` | Reasoning tokens are a subset of completion tokens and output stays full | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:35` |
| `test_record_missing_usage_entirely_yields_nothing` | Record missing usage entirely yields nothing | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:43` |
| `test_record_with_zero_usage_yields_nothing` | Record with zero usage yields nothing | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:48` |
| `test_provider_field_is_lowercased` | Provider field is lowercased | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:53` |
| `test_provider_defaults_to_none` | Provider defaults to none | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:59` |
| `test_response_nested_under_response_key_is_parsed` | Response nested under response key is parsed | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:65` |
| `test_request_id_matches_the_record_id` | Request id matches the record id | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:74` |
| `test_session_id_falls_back_to_file_stem` | Session id falls back to file stem | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:82` |
| `test_files_a_and_b_each_yield_one_event_with_the_same_request_id` | Files a and b each yield one event with the same request id | `tests/test_openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:88` |
| `test_step_finish_parts_are_summed_not_the_overwritten_message_tokens` | Step finish parts are summed not the overwritten message tokens | `tests/test_opencode.py` | [[tests/test_opencode.py]] `tests/test_opencode.py:150` |
| `test_field_mapping_of_one_event` | Field mapping of one event | `tests/test_opencode.py` | [[tests/test_opencode.py]] `tests/test_opencode.py:162` |
| `test_text_content_never_reaches_events` | Text content never reaches events | `tests/test_opencode.py` | [[tests/test_opencode.py]] `tests/test_opencode.py:184` |
| `test_message_without_step_finish_falls_back_to_message_tokens` | Message without step finish falls back to message tokens | `tests/test_opencode.py` | [[tests/test_opencode.py]] `tests/test_opencode.py:189` |
%% generated:chunk-tests end %%
