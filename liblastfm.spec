Summary:	Library to access Last.fm features
Name:		liblastfm
Version:	1.0.9
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	https://github.com/lastfm/liblastfm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8748f423f66f2fbc38c39f9153d01a71
Patch0:		%{name}-ruby19.patch
URL:		https://github.com/lastfm/liblastfm
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtXml-devel
BuildRequires:	cmake >= 2.8.6
BuildRequires:	fftw3-single-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	ruby
BuildRequires:	ruby-modules
BuildRequires:	sed >= 4.0
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
%setup -q
#%patch0 -p0

%build
install -d build
cd build
%cmake \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DBUILD_FINGERPRINT:BOOL=ON \
	..

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.1
%attr(755,root,root) %{_libdir}/%{name}_fingerprint.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}_fingerprint.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%attr(755,root,root) %{_libdir}/%{name}_fingerprint.so
%{_includedir}/lastfm
