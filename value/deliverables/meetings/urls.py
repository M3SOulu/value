# coding: utf-8

from django.conf.urls import url

from value.deliverables.meetings import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<meeting_id>\d+)/$', views.meeting, name='meeting'),
    url(r'^(?P<meeting_id>\d+)/status/$', views.change_meeting_status, name='change_meeting_status'),
    url(r'^(?P<meeting_id>\d+)/progress/$', views.update_meeting_progress, name='update_meeting_progress'),
    url(r'^(?P<meeting_id>\d+)/rationales/$', views.rationales, name='rationales'),
    url(r'^(?P<meeting_id>\d+)/sync-jira/$', views.sync_jira, name='sync_jira'),
    url(r'^(?P<meeting_id>\d+)/export/$', views.export_excel, name='export_excel'),

    # Evaluate URLs
    url(r'^(?P<meeting_id>\d+)/evaluate/$', views.evaluate, name='evaluate'),
    url(r'^(?P<meeting_id>\d+)/evaluate/save/$', views.save_evaluation, name='save_evaluation'),
    url(r'^(?P<meeting_id>\d+)/evaluate/rationale/save/$', views.save_rationale, name='save_rationale'),

    # Rationale URLs
    url(r'^(?P<meeting_id>\d+)/rationale/item/(?P<meeting_item_id>\d+)/$', views.meeting_item_rationale,
        name='meeting_item_rationale'),
    url(r'^(?P<meeting_id>\d+)/rationale/scenario/(?P<scenario_id>\d+)/$', views.scenario_rationale,
        name='scenario_rationale'),

    # Dashboard URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/$', views.dashboard, name='dashboard'),

    # Summary Charts URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/factors-usage/$', views.dashboard_factors_usage_chart,
        name='dashboard_factors_usage_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/stakeholders-input/$', views.dashboard_stakeholders_input_chart,
        name='dashboard_stakeholders_input_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/ranking/$', views.value_ranking, name='value_ranking'),
    url(r'^(?P<meeting_id>\d+)/dashboard/ranking/groups/$', views.value_ranking_groups, name='value_ranking_groups'),
    url(r'^(?P<meeting_id>\d+)/dashboard/ranking/individual/$', views.value_ranking_individual, name='value_ranking_individual'),

    url(r'^(?P<meeting_id>\d+)/dashboard/items/$', views.decision_items_overview, name='decision_items_overview'),
    url(r'^(?P<meeting_id>\d+)/dashboard/measures/$', views.features_comparison, name='features_comparison'),
    url(r'^(?P<meeting_id>\d+)/dashboard/measures/(?P<measure_value_id>\d+)/$', views.features_comparison_chart,
        name='features_comparison_chart'),

    url(r'^(?P<meeting_id>\d+)/dashboard/analysis/$', views.decision_analysis, name='decision_analysis'),

    # Meta Charts
    url(r'^(?P<meeting_id>\d+)/dashboard/agreement/$', views.stakeholders_agreement, name='stakeholders_agreement'),
    url(r'^(?P<meeting_id>\d+)/dashboard/agreement/details/factors/$', views.stakeholders_agreement_details_factors,
        name='stakeholders_agreement_details_factors'),
    url(r'^(?P<meeting_id>\d+)/dashboard/agreement/grouped/$', views.stakeholders_agreement_grouped,
        name='stakeholders_agreement_grouped'),
    url(r'^(?P<meeting_id>\d+)/dashboard/agreement/grouped/details/factors/$', views.stakeholders_agreement_grouped_details_factors,
        name='stakeholders_agreement_grouped_details_factors'),

    # Stakeholders Individual Opinion
    url(r'^(?P<meeting_id>\d+)/dashboard/opinion/$', views.stakeholders_opinion, name='stakeholders_opinion'),
    url(r'^(?P<meeting_id>\d+)/dashboard/opinion/grouped/$', views.stakeholders_opinion_grouped,
        name='stakeholders_opinion_grouped'),

    # Priority List
    url(r'^(?P<meeting_id>\d+)/dashboard/priority/$', views.priority_list, name='priority_list'),
    url(r'^(?P<meeting_id>\d+)/dashboard/priority/results/$', views.priority_list_results, name='priority_list_results'),

    # Detailed Charts URLs
    # Factors Comparison URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/$', views.features, name='features'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/(?P<meeting_item_id>\d+)/$', views.features_chart,
        name='features_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/scenarios/$', views.features_scenarios,
        name='features_scenarios'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/scenarios/(?P<scenario_id>\d+)/$', views.features_scenario_chart,
        name='features_scenario_chart'),

    # Factors Groups Comparison URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/$', views.factors_groups, name='factors_groups'),
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/(?P<meeting_item_id>\d+)/$', views.factors_groups_chart,
        name='factors_groups_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/scenarios/$', views.factors_groups_scenarios,
        name='factors_groups_scenarios'),
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/scenarios/(?P<scenario_id>\d+)/$', views.factors_groups_scenario_chart,
        name='factors_groups_scenario_chart'),

    # Decision Items Acceptance URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/$', views.features_acceptance, name='features_acceptance'),
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/(?P<meeting_item_id>\d+)/$', views.features_acceptance_chart,
        name='features_acceptance_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/scenarios/$', views.features_acceptance_scenarios,
        name='features_acceptance_scenarios'),
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/scenarios/(?P<scenario_id>\d+)/$',
        views.features_acceptance_scenario_chart, name='features_acceptance_scenario_chart'),

    # Scenarios URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/add/$', views.add_scenario, name='add_scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/builder/$', views.scenario_builder, name='scenario_builder'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/delete/$', views.delete_scenario, name='delete_scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/compare/$', views.compare_scenario, name='compare_scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/(?P<scenario_id>\d+)/$', views.scenario, name='scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/(?P<scenario_id>\d+)/overview/$', views.scenario_overview_chart,
        name='scenario_overview_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/(?P<scenario_id>\d+)/value_ranking/$',
        views.scenario_value_ranking_chart, name='scenario_value_ranking_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/(?P<scenario_id>\d+)/edit/$', views.edit_scenario,
        name='edit_scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/(?P<scenario_id>\d+)/details/$', views.scenario_details,
        name='scenario_details'),

    # Final Decision URLs
    url(r'^(?P<meeting_id>\d+)/decision/$', views.final_decision, name='final_decision'),
    url(r'^(?P<meeting_id>\d+)/decision/save/$', views.save_final_decision, name='save_final_decision'),
    url(r'^(?P<meeting_id>\d+)/decision/set-scenario/$', views.set_scenario_final_decision, name='set_scenario_final_decision'),
    url(r'^(?P<meeting_id>\d+)/decision/rationale/save/$', views.save_final_decision_rationale,
        name='save_final_decision_rationale'),
    url(r'^(?P<meeting_id>\d+)/decision/rationale/item/(?P<meeting_item_id>\d+)/save/$',
        views.save_final_decision_item_rationale, name='save_final_decision_item_rationale'),

    # Meeting Settings URLs
    url(r'^(?P<meeting_id>\d+)/settings/$', views.settings, name='settings'),
    url(r'^(?P<meeting_id>\d+)/settings/delete/$', views.delete, name='delete'),
    url(r'^(?P<meeting_id>\d+)/settings/items/$', views.decision_items, name='decision_items'),
    url(r'^(?P<meeting_id>\d+)/settings/items/add/$', views.add_decision_items, name='add_decision_items'),
    url(r'^(?P<meeting_id>\d+)/settings/items/remove/$', views.remove_decision_items, name='remove_decision_items'),
    url(r'^(?P<meeting_id>\d+)/settings/stakeholders/$', views.stakeholders, name='stakeholders'),
    url(r'^(?P<meeting_id>\d+)/settings/stakeholders/add/$', views.add_stakeholders, name='add_stakeholders'),
    url(r'^(?P<meeting_id>\d+)/settings/stakeholders/remove/$', views.remove_stakeholder, name='remove_stakeholder'),
    url(r'^(?P<meeting_id>\d+)/settings/stakeholders/remove-idle/$', views.remove_idle_stakeholders, name='remove_idle_stakeholders')
]
