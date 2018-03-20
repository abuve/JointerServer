from django.conf.urls import url

from cmdb.views import server
from cmdb.views import approval
from cmdb.views import docker
from cmdb.views import business
from cmdb.views import idc
from cmdb.views import dashboard

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', dashboard.DashBoardIndexView.as_view(), name='dashboard'),
    url(r'dashboard.html$', dashboard.DashBoardIndexView.as_view(), name='dashboard'),
    url(r'dashboard_chart_ajax/', dashboard.DashBoardChartAjaxView.as_view(), name='dashboard-chart-ajax'),

    url(r'^server-list.html$', server.ServerListView.as_view(), name='cmdb-server-list'),
    url(r'^server-json.html$', server.ServerJsonView.as_view(), name='cmdb-server-json'),

    url(r'^asset-create.html$', server.AssetCreateView.as_view(), name='cmdb-asset-create'),

    url(r'^docker-list.html$', docker.DockerListView.as_view(), name='cmdb-docker-list'),
    url(r'^docker-json.html$', docker.DockerJsonView.as_view(), name='cmdb-docker-json'),

    url(r'^asset-detail-(?P<asset_nid>\d+).html$', server.AssetDetailView.as_view(), name='cmdb-asset-detail'),

    url(r'^approval-list.html$', approval.ApprovalListView.as_view(), name='cmdb-approval-list'),
    url(r'^approval-json.html$', approval.ApprovalJsonView.as_view(), name='cmdb-approval-json'),

    url(r'^business-list.html$', business.BusinessListView.as_view(), name='cmdb-business-list'),
    url(r'^business-json.html$', business.BusinessJsonView.as_view(), name='cmdb-business-json'),
    url(r'^business-detail-(?P<business_nid>\d+).html$', business.BusinessDetailView.as_view(), name='cmdb-business-detail'),

    # cmdb report with no asset id, it's need admin to approved.
    url(r'^report/asset_report_use_asset_id/$', approval.asset_report_use_asset_id),
    url(r'^report/asset_report_with_no_id/$', approval.asset_with_no_asset_id),

    url(r'^idc-list.html$', idc.IdcListView.as_view(), name='cmdb-idc-list'),
    url(r'^idcs.html$', idc.IdcJsonView.as_view(), name='cmdb-idcs'),
    url(r'^add-idc.html$', idc.AddIdcView.as_view(), name='cmdb-add-idc'),
    url(r'^edit-idc-(?P<idc_nid>\d+).html$', idc.UpdateIdcView.as_view(), name='cmdb-edit-idc'),

    url(r'^get_instance_by_asset_id/$', approval.asset_with_no_asset_id, name='cmdb-get-instance-by-asset-id'),

    url(r'^test/$', server.test),

]
