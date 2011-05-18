
%define _mochiwebver r113
%define _ibrowsever 2.1.2

Summary:	Apache CouchDB
Name:		apache-couchdb
Version:	1.0.2
Release:	0.1
License:	Apache v2.0
Group:		Applications
Source0:	http://www.apache.org/dist/couchdb/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7ffbbe0f23f672181c89923c9f7a1de1
Source1:	%{name}.init
URL:		http://couchdb.apache.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.6.3
BuildRequires:	curl-devel
BuildRequires:	erlang >= 1:R12B5
BuildRequires:	help2man
BuildRequires:	js-devel
BuildRequires:	libicu-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	erlang >= 1:R12B5
Requires:	libicu-devel
Requires:	pkgconfig
# these came from readme, need to check if these are really needed
#Requires:	Mozilla-SpiderMonkey
#Requires:	gcc
#Requires:	make
#Requires:	openssl
Provides:	group(couchdb)
Provides:	user(couchdb)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache CouchDB is a distributed, fault-tolerant and schema-free
document-oriented database accessible via a RESTful HTTP/JSON API.
Among other features, it provides robust, incremental replication with
bi-directional conflict detection and resolution, and is queryable and
indexable using a table-oriented view engine with JavaScript acting as
the default view definition language.

%prep
%setup -q

%build

%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/couchdb
install -d $RPM_BUILD_ROOT/var/log/couchdb

install -d $RPM_BUILD_ROOT/etc/sysconfig
mv $RPM_BUILD_ROOT/etc/default/couchdb $RPM_BUILD_ROOT/etc/sysconfig

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/couchdb

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 203 -r -f couchdb
%useradd -u 203 -r -d /var/lib/couchdb -s /bin/sh -c "CouchDB Administrator" -g couchdb couchdb

%post
/sbin/chkconfig --add couchdb
%service couchdb restart

%preun
if [ "$1" = "0" ]; then
	%service -q couchdb stop
	/sbin/chkconfig --del couchdb
fi

%postun
if [ "$1" = "0" ]; then
	%userremove couchdb
	%groupremove couchdb
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CHANGES NEWS NOTICE README THANKS
%dir %{_sysconfdir}/couchdb
%dir %{_sysconfdir}/couchdb/default.d
%attr(755,couchdb,couchdb) %{_sysconfdir}/couchdb/default.d
%attr(755,couchdb,couchdb) %dir %{_sysconfdir}/couchdb/local.d
%attr(644,couchdb,couchdb) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/couchdb/default.ini
%attr(644,couchdb,couchdb) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/couchdb/local.ini
# XXX -> sysconfdir
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/couchdb
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/couchdb
%attr(754,root,root) /etc/rc.d/init.d/couchdb

%dir /var/log/couchdb
%attr(755,couchdb,couchdb) /var/log/couchdb

# XXX: sbindir?
%attr(755,root,root) %{_bindir}/couchdb
%attr(755,root,root) %{_bindir}/couchjs
%{_mandir}/man1/couchdb.1*
%{_mandir}/man1/couchjs.1*

%dir %{_libdir}/couchdb

%dir %{_libdir}/couchdb/bin
%attr(755,root,root) %{_libdir}/couchdb/bin/couchjs

%dir %{_libdir}/couchdb/erlang
%dir %{_libdir}/couchdb/erlang/lib
# XXX: better have unversioned dirs?
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/ebin
%{_libdir}/couchdb/erlang/lib/couch-%{version}/ebin/*.beam
%{_libdir}/couchdb/erlang/lib/couch-%{version}/ebin/*.app
# XXX check if this include is needed runtime
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/include
%{_libdir}/couchdb/erlang/lib/couch-%{version}/include/couch_db.hrl

# XXX: check if .la is needed
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/priv
%{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/couchspawnkillable

%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/lib
%{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/lib/couch_icu_driver.la
%attr(755,root,root) %{_libdir}/couchdb/erlang/lib/couch-%{version}/priv/lib/couch_icu_driver.so
/usr/lib64/couchdb/erlang/lib/couch-1.0.2/include/couch_js_functions.hrl
/usr/lib64/couchdb/erlang/lib/couch-1.0.2/priv/stat_descriptions.cfg

# XXX: better have unversioned dirs?
%dir %{_libdir}/couchdb/erlang/lib/mochiweb-%{_mochiwebver}
%dir %{_libdir}/couchdb/erlang/lib/mochiweb-%{_mochiwebver}/ebin
%{_libdir}/couchdb/erlang/lib/mochiweb-%{_mochiwebver}/ebin/*.beam
%{_libdir}/couchdb/erlang/lib/mochiweb-%{_mochiwebver}/ebin/*.app

%dir %{_libdir}/couchdb/erlang/lib/etap
%{_libdir}/couchdb/erlang/lib/etap/ebin

%dir %{_libdir}/couchdb/erlang/lib/erlang-oauth
%{_libdir}/couchdb/erlang/lib/erlang-oauth/ebin

%dir %{_libdir}/couchdb/erlang/lib/ibrowse-%{_ibrowsever}
%{_libdir}/couchdb/erlang/lib/ibrowse-%{_ibrowsever}/ebin

%attr(755,couchdb,couchdb) %{_datadir}/couchdb
