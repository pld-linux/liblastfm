Summary:	Library to access Last.fm features
Name:		liblastfm
Version:	0.3.3
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	http://github.com/mxcl/%{name}/tarball/%{version}#/%{name}-%{version}.tar.gz
# Source0-md5:	fe339bf46aefc515c251200d10262f79
Patch0:		%{name}-ruby19.patch
URL:		http://github.com/mxcl/liblastfm/
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtXml-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	ruby
BuildRequires:	ruby-modules
BuildRequires:	which
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
%setup -q -n mxcl-liblastfm-1c739eb
%patch0 -p0

find . -name *.pro -exec sed -i -e "/target.path/s/lib/%{_lib}/g" {} \;

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
