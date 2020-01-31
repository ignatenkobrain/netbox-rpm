Name:           netbox
Version:        2.7.3
Release:        1%{?dist}
Summary:        IP address management (IPAM) and data center infrastructure management (DCIM)

License:        ASL 2.0 and MIT and OFL
URL:            https://github.com/netbox-community/netbox/
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        netbox.service
Source2:        netbox-rq.service

BuildRequires:  python3-devel
BuildRequires:  systemd-rpm-macros
Requires:       /usr/bin/gunicorn
Requires(pre):  shadow-utils
# base_requirements.txt
Requires:       python%{python3_version}dist(django)
Requires:       python%{python3_version}dist(django-cacheops)
Requires:       python%{python3_version}dist(django-cors-headers)
Requires:       python%{python3_version}dist(django-debug-toolbar)
Requires:       python%{python3_version}dist(django-filter)
Requires:       python%{python3_version}dist(django-mptt)
Requires:       python%{python3_version}dist(django-prometheus)
Requires:       python%{python3_version}dist(django-rq)
Requires:       python%{python3_version}dist(django-tables2)
Requires:       python%{python3_version}dist(django-taggit)
Requires:       python%{python3_version}dist(django-taggit-serializer)
Requires:       python%{python3_version}dist(django-timezone-field)
Requires:       python%{python3_version}dist(djangorestframework)
Requires:       python%{python3_version}dist(drf-yasg/validation)
Requires:       python%{python3_version}dist(jinja2)
Requires:       python%{python3_version}dist(netaddr)
Requires:       python%{python3_version}dist(pillow)
# originally: psycopg2
Requires:       python%{python3_version}dist(psycopg2)
Requires:       python%{python3_version}dist(py-gfm)
# originally: pycryptodome
Requires:       python%{python3_version}dist(pycryptodomex)
Requires:       python%{python3_version}dist(pyyaml)
Requires:       python%{python3_version}dist(redis)
Requires:       python%{python3_version}dist(svgwrite)
Recommends:     python%{python3_version}dist(django-storages)
# netbox/project-static/bootstrap-*-dist/
# License(s): MIT
Provides:       bundled(js-bootstrap) = 3.4.1
# netbox/project-static/clipboard.js/
# License(s): MIT
Provides:       bundled(js-clipboard) = 2.0.4
# netbox/project-static/flatpickr-*/
# License(s): MIT
Provides:       bundled(js-flatpickr) = 4.6.3
# netbox/project-static/font-awesome-*/
# License(s): OFL and MIT
Provides:       bundled(fontawesome-fonts) = 4.7.0
# netbox/project-static/jquery/
# License(s): MIT
Provides:       bundled(js-jquery) = 3.4.1
# netbox/project-static/jquery-ui-*/
# License(s): MIT
Provides:       bundled(js-jquery-ui) = 1.12.1
# netbox/project-static/select2-*/
# License(s): MIT
Provides:       bundled(js-select2) = 4.0.12
# netbox/project-static/select2-bootstrap-*/
# License(s): MIT
Provides:       bundled(js-select2-bootstrap-theme) = 0.1.0~beta10

%description
NetBox is an IP address management (IPAM)
and data center infrastructure management (DCIM) tool.
Initially conceived by the network engineering team at DigitalOcean,
NetBox was developed specifically to address the needs of network
and infrastructure engineers. It is intended to function
as a domain-specific source of truth for network operations.

%prep
%autosetup
find -type f -name '*.py' \
  -exec sed -i -e 's/from Crypto\./from Cryptodome./' '{}' + \
  -exec pathfix.py -pni '%python3 %{py3_shbang_opts}' '{}' + \
  %{nil}
find netbox/project-static/ -type f -executable -exec chmod -x '{}' +

%install
install -Dpm0644 -t %{buildroot}%{_unitdir} %{S:1}
install -Dpm0644 -t %{buildroot}%{_unitdir} %{S:2}
install -Dpm0640 netbox/netbox/configuration.example.py %{buildroot}%{_sysconfdir}/netbox/configuration.py
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/netbox contrib/gunicorn.py

mkdir -p %{buildroot}{%{_datadir},%{_sysconfdir}/netbox}
cp -a netbox %{buildroot}%{_datadir}
rm -v %{buildroot}%{_datadir}/netbox/netbox/configuration.example.py

%py_byte_compile %python3 %{buildroot}%{_datadir}/netbox
# This is done later to avoid byte-compilation
ln -srf %{_sysconfdir}/netbox/configuration.py %{buildroot}%{_datadir}/netbox/netbox/configuration.py

%pre
getent group netbox >/dev/null || groupadd -r netbox
getent passwd netbox >/dev/null || \
    useradd -r -g netbox -d %{_datadir}/netbox -s /bin/bash \
    -c "NetBox user" netbox
exit 0

%files
%license LICENSE.txt NOTICE
%doc README.md CHANGELOG.md
%{_datadir}/netbox/
%{_unitdir}/netbox.service
%{_unitdir}/netbox-rq.service
%defattr(-,netbox,netbox)
%dir %{_sysconfdir}/netbox/
%config(noreplace) %{_sysconfdir}/netbox/configuration.py
%config(noreplace) %{_sysconfdir}/netbox/gunicorn.py

%changelog
* Fri Jan 31 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.7.3-1
- Initial package
