Summary:	Library to access Last.fm features
Name:		liblastfm
Version:	0.3.0
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	http://cdn.last.fm/src/%{name}-%{version}.tar.bz2
# Source0-md5:	3f73222ebc31635941832b01e7a494b6
Patch0:		%{name}-path.patch
URL:		http://last.fm
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtXml-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	qt4-qmake
BuildRequires:	ruby
BuildRequires:	ruby-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
liblastfm is a collection of libraries to help you integrate Last.fm
services into your rich desktop software. It is officially supported
software developed by Last.fm staff.

%package devel
Summary:	Header files for %{name}
Summary(pl.UTF-8):	Pliki nagłówkowe %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name}.

%description devel -l pl.UTF-8
Pliki nagłówkowe %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--prefix %{_prefix} \
	--libdir %{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.?
%attr(755,root,root) %{_libdir}/%{name}_fingerprint.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}_fingerprint.so.?

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%attr(755,root,root) %{_libdir}/%{name}_fingerprint.so
%{_includedir}/lastfm
%{_includedir}/lastfm.h
