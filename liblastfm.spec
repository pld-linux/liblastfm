# NOTE:
# - qt5 build fails to find files if rpm BUILD dir is symlink
#
# Conditional build:
%bcond_without	qt4		# Qt4
%bcond_without	qt5		# Qt5

Summary:	Library to access Last.fm features
Name:		liblastfm
Version:	1.0.9
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	https://github.com/lastfm/liblastfm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8748f423f66f2fbc38c39f9153d01a71
URL:		https://github.com/lastfm/liblastfm
BuildRequires:	cmake >= 2.8.6
BuildRequires:	fftw3-single-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	pkgconfig
BuildRequires:	ruby
BuildRequires:	ruby-modules
BuildRequires:	sed >= 4.0
BuildRequires:	which
%if %{with qt4}
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtXml-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Sql-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# includedir files "conflict"
%define		_duplicate_files_terminate_build   0

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

%package qt5
Summary:	Qt5 libraries to integrate Last.fm services
Group:		Libraries

%description qt5
Qt5 libraries to integrate Last.fm services.


%package qt5-devel
Summary:	Development files for liblastfm-qt5
Requires:	%{name}-qt5 = %{version}-%{release}

%description qt5-devel
Development files for liblastfm-qt5.

%prep
%setup -q

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DBUILD_FINGERPRINT:BOOL=ON \
	..
%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake \
	-DBUILD_WITH_QT4:BOOL=OFF \
	-DBUILD_FINGERPRINT:BOOL=ON \
	..
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with qt4}
%{__make} -C build-qt4 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with qt5}
%{__make} -C build-qt5 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/liblastfm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm.so.1
%attr(755,root,root) %{_libdir}/liblastfm_fingerprint.so.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm_fingerprint.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%attr(755,root,root) %{_libdir}/%{name}_fingerprint.so
%{_includedir}/lastfm
%endif

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/liblastfm5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm5.so.1
%attr(755,root,root) %{_libdir}/liblastfm_fingerprint5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm_fingerprint5.so.1

%files qt5-devel
%defattr(644,root,root,755)
%{_libdir}/liblastfm5.so
%{_libdir}/liblastfm_fingerprint5.so
%{_includedir}/lastfm
%endif
