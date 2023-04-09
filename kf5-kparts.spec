#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.105
%define		qtver		5.15.2
%define		kfname		kparts

Summary:	Plugin framework for user interface components
Name:		kf5-%{kfname}
Version:	5.105.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	088ec7dd5877fffe19c8214fa24325b0
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	kf5-kiconthemes-devel >= %{version}
BuildRequires:	kf5-kio-devel >= %{version}
BuildRequires:	kf5-kjobwidgets-devel >= %{version}
BuildRequires:	kf5-kservice-devel >= %{version}
BuildRequires:	kf5-ktextwidgets-devel >= %{version}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf5-kxmlgui-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5Xml >= %{qtver}
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{version}
Requires:	kf5-kcoreaddons >= %{version}
Requires:	kf5-ki18n >= %{version}
Requires:	kf5-kiconthemes >= %{version}
Requires:	kf5-kio >= %{version}
Requires:	kf5-kjobwidgets >= %{version}
Requires:	kf5-kservice >= %{version}
Requires:	kf5-kwidgetsaddons >= %{version}
Requires:	kf5-kxmlgui >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
This library implements the framework for KDE parts, which are
elaborate widgets with a user-interface defined in terms of actions
(menu items, toolbar icons).

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf5-kio-devel >= %{version}
Requires:	kf5-ktextwidgets-devel >= %{version}
Requires:	kf5-kxmlgui-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5Parts.so.5
%attr(755,root,root) %{_libdir}/libKF5Parts.so.*.*
#%%attr(755,root,root) %{qt5dir}/plugins/spellcheckplugin.so
%{_datadir}/kservicetypes5/browserview.desktop
%{_datadir}/kservicetypes5/kpart.desktop
%{_datadir}/kdevappwizard/templates/kpartsapp.tar.bz2
%{_datadir}/kservicetypes5/kparts-readonlypart.desktop
%{_datadir}/kservicetypes5/kparts-readwritepart.desktop
%{_datadir}/qlogging-categories5/kparts.categories


%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KParts
%{_libdir}/cmake/KF5Parts
%{_libdir}/libKF5Parts.so
%{qt5dir}/mkspecs/modules/qt_KParts.pri
