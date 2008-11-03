Summary:	Apache CouchDB
Name:		apache-couchdb
Version:	0.8.1
Release:	0.1
License:	Apache v2.0
Group:		Applications
Source0:	http://www.apache.org/dist/incubator/couchdb/%{version}-incubating/%{name}-%{version}-incubating.tar.gz
# Source0-md5:	89e037b370bef33be93f0f317e07615f
URL:		http://incubator.apache.org/couchdb/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.6.3
BuildRequires:	erlang >= 1:R11B
BuildRequires:	help2man
BuildRequires:	js-devel
BuildRequires:	libicu-devel
BuildRequires:	libtool
Requires:	Mozilla-SpiderMonkey
Requires:	erlang >= 1:R11B
Requires:	gcc
Requires:	make
Requires:	openssl
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 203 -r -f couchdb
%useradd -u 203 -r -d /var/lib/couchdb -s /bin/sh -c "CouchDB Administrator" -g couchdb couchdb

%postun
if [ "$1" = "0" ]; then
	%userremove couchdb
	%groupremove couchdb
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CHANGES NEWS NOTICE README THANKS
