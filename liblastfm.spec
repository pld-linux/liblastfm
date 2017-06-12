# NOTE:
# - qt5 build fails to find files if rpm BUILD dir is symlink
#
# Conditional build:
%bcond_without	qt4		# Qt4 based library
%bcond_without	qt5		# Qt5 based library
%bcond_without	fingerprint	# liblastfm_fingerprint libraries

Summary:	Qt4 based library to access Last.fm features
Summary(pl.UTF-8):	Oparta na Qt4 biblioteka pozwalająca na dostep do funkcjonalności Last.fm
Name:		liblastfm
Version:	1.0.9
Release:	2
License:	GPL v3
Group:		Libraries
#Source0Download: https://github.com/lastfm/liblastfm/releases
Source0:	https://github.com/lastfm/liblastfm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8748f423f66f2fbc38c39f9153d01a71
URL:		https://github.com/lastfm/liblastfm
BuildRequires:	cmake >= 2.8.6
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
%if %{with fingerprint}
BuildRequires:	fftw3-single-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	pkgconfig
%endif
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4.8
BuildRequires:	QtDBus-devel >= 4.8
BuildRequires:	QtNetwork-devel >= 4.8
BuildRequires:	QtTest-devel >= 4.8
BuildRequires:	QtXml-devel >= 4.8
BuildRequires:	qt4-build >= 4.8
BuildRequires:	qt4-qmake >= 4.8
%if %{with fingerprint}
BuildRequires:	QtSql-devel >= 4.8
%endif
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5DBus-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%if %{with fingerprint}
BuildRequires:	Qt5Sql-devel >= 5
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# shared include files
%define		_duplicate_files_terminate_build   0

%description
liblastfm is a collection of libraries to help you integrate Last.fm
services into your rich desktop software. It is officially supported
software developed by Last.fm staff.

This package contains Qt 4 based libraries.

%description -l pl.UTF-8
liblastfm to zbiór bibliotek pomocnych przy integrowaniu usług Last.fm
z oprogramowaniem komputerowym. Jest to oficjalnie wspierane
oprogramowanie tworzone przez pracowników Last.fm.

Ten pakiet zawiera biblioteki oparte na Qt 4.

%package devel
Summary:	Header files for Qt4 based liblastfm libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek liblastfm opartych na Qt4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4.8
Requires:	QtNetwork-devel >= 4.8
Requires:	QtXml-devel >= 4.8
Requires:	libstdc++-devel

%description devel
Header files for Qt4 based liblastfm libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek liblastfm opartych na Qt4.

%package qt5
Summary:	Qt5 based library to access Last.fm features
Summary(pl.UTF-8):	Oparta na Qt5 biblioteka pozwalająca na dostep do funkcjonalności Last.fm
Group:		Libraries

%description qt5
liblastfm is a collection of libraries to help you integrate Last.fm
services into your rich desktop software. It is officially supported
software developed by Last.fm staff.

This package contains Qt 4 based libraries.

%description qt5 -l pl.UTF-8
liblastfm to zbiór bibliotek pomocnych przy integrowaniu usług Last.fm
z oprogramowaniem komputerowym. Jest to oficjalnie wspierane
oprogramowanie tworzone przez pracowników Last.fm.

Ten pakiet zawiera biblioteki oparte na Qt 5.

%package qt5-devel
Summary:	Header files for Qt5 based liblastfm libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek liblastfm opartych na Qt5
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	Qt5Core-devel >= 5
Requires:	Qt5Network-devel >= 5
Requires:	Qt5Xml-devel >= 5
Requires:	libstdc++-devel

%description qt5-devel
Header files for Qt5 based liblastfm libraries.

%description qt5-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek liblastfm opartych na Qt4.

%prep
%setup -q

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DBUILD_FINGERPRINT:BOOL=%{?with_fingerprint:ON}%{!?with_fingerprint:OFF} \
	..
%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake \
	-DBUILD_WITH_QT4:BOOL=OFF \
	-DBUILD_FINGERPRINT:BOOL=%{?with_fingerprint:ON}%{!?with_fingerprint:OFF} \
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	qt5 -p /sbin/ldconfig
%postun	qt5 -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/liblastfm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm.so.1
%if %{with fingerprint}
%attr(755,root,root) %{_libdir}/liblastfm_fingerprint.so.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm_fingerprint.so.1
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%if %{with fingerprint}
%attr(755,root,root) %{_libdir}/%{name}_fingerprint.so
%endif
%{_includedir}/lastfm
%endif

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/liblastfm5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm5.so.1
%if %{with fingerprint}
%attr(755,root,root) %{_libdir}/liblastfm_fingerprint5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblastfm_fingerprint5.so.1
%endif

%files qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblastfm5.so
%if %{with fingerprint}
%attr(755,root,root) %{_libdir}/liblastfm_fingerprint5.so
%endif
%{_includedir}/lastfm
%endif
