Summary:	Apache CouchDB
Name:		apache-couchdb
Version:	0.8.1
Release:	0.1
License:	Apache v2.0
Group:		Applications
Source0:	http://www.apache.org/dist/incubator/couchdb/%{version}-incubating/%{name}-%{version}-incubating.tar.gz
# Source0-md5:	89e037b370bef33be93f0f317e07615f
Patch0:		%{name}-init.d.patch
URL:		http://incubator.apache.org/couchdb/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.6.3
BuildRequires:	erlang >= 1:R11B
BuildRequires:	help2man
BuildRequires:	js-devel
BuildRequires:	libicu-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	erlang >= 1:R11B
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
%setup -q -n %{name}-%{version}-incubating
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/couchdb/couch.ini
# XXX -> sysconfdir
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/couchdb
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/couchdb
%attr(754,root,root) /etc/rc.d/init.d/couchdb

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
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating
%dir %{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating/ebin
%{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating/ebin/*.beam
%{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating/ebin/*.app
# XXX check if this include is needed runtime
%{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating/include/couch_db.hrl
# XXX: check if .la is needed
%{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating/priv/lib/couch_erl_driver.la
%attr(755,root,root) %{_libdir}/couchdb/erlang/lib/couch-%{version}-incubating/priv/lib/couch_erl_driver.so
# XXX: better have unversioned dirs?
%dir %{_libdir}/couchdb/erlang/lib/mochiweb-r82
%dir %{_libdir}/couchdb/erlang/lib/mochiweb-r82/ebin
%{_libdir}/couchdb/erlang/lib/mochiweb-r82/ebin/*.beam
%{_libdir}/couchdb/erlang/lib/mochiweb-r82/ebin/*.app
%{_datadir}/couchdb
