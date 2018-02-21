from django.conf.urls import url

from cmdb.views import server
from cmdb.views import approval
from cmdb.views import docker
from cmdb.views import business
from cmdb.views import idc

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^server-list.html$', login_required(server.ServerListView.as_view())),
    url(r'^server-json.html$', login_required(server.ServerJsonView.as_view())),

    url(r'^asset-create.html$', login_required(server.AssetCreateView.as_view())),

    url(r'^docker-list.html$', login_required(docker.DockerListView.as_view())),
    url(r'^docker-json.html$', login_required(docker.DockerJsonView.as_view())),

    url(r'^asset-detail-(?P<asset_nid>\d+).html$', login_required(server.AssetDetailView.as_view())),

    url(r'^approval-list.html$', login_required(approval.ApprovalListView.as_view())),
    url(r'^approval-json.html$', login_required(approval.ApprovalJsonView.as_view())),

    url(r'^business-list.html$', login_required(business.BusinessListView.as_view())),
    url(r'^business-json.html$', login_required(business.BusinessJsonView.as_view())),
    url(r'^business-detail-(?P<business_nid>\d+).html$', login_required(business.BusinessDetailView.as_view())),

    # cmdb report with no asset id, it's need admin to approved.
    url(r'^report/asset_report_use_asset_id/$', approval.asset_report_use_asset_id),
    url(r'^report/asset_report_with_no_id/$', approval.asset_with_no_asset_id),

    url(r'^idc-list.html$', login_required(idc.IdcListView.as_view())),
    url(r'^idcs.html$', login_required(idc.IdcJsonView.as_view())),
    url(r'^add-idc.html$', login_required(idc.AddIdcView.as_view())),
    url(r'^edit-idc-(?P<idc_nid>\d+).html$', login_required(idc.UpdateIdcView.as_view())),

    url(r'^get_instance_by_asset_id/$', login_required(approval.asset_with_no_asset_id)),

    # url(r'^test/$', server.test),

]
