#
# Conditional build:
%bcond_without	bonobo	# bonobo support
%bcond_without	gnome	# GNOME documentation displaying support
%bcond_with	gimp	# GIMP plugin
#
Summary:	GTKam - graphical frontend for gphoto2
Summary(pl.UTF-8):	GTKam - graficzny interfejs do gphoto2
Name:		gtkam
Version:	1.1
Release:	1
License:	LGPL v2+
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
# Source0-md5:	7c7ed105e97485a3551c13ecbc932e44
Patch0:		%{name}-paths.patch
Patch1:		intltool.patch
URL:		http://www.gphoto.org/proj/gtkam/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14.1
BuildRequires:	gettext-tools >= 0.19.7
%{?with_gimp:BuildRequires:	gimp-devel >= 1:2.0}
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	intltool
%{?with_bonobo:BuildRequires:	libbonoboui-devel >= 2.0}
BuildRequires:	libexif-devel >= 0.3.2
BuildRequires:	libexif-gtk-devel
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.0}
BuildRequires:	libgphoto2-devel >= 2.5.0
BuildRequires:	libtool >= 2:2
%{?with_gimp:BuildRequires:	libusb-compat-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	scrollkeeper
Requires:	libgphoto2 >= 2.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with gimp}
%define		gimpplugindir	%(gimptool --gimpplugindir)/plug-ins
%endif

%description
The gtkam package provides a GTK+-based frontend to gphoto2.

%description -l pl.UTF-8
Pakiet gtkam udostępnia oparty o GTK+ graficzny interfejs do gphoto2.

%package -n gimp-plugin-gtkam
Summary:	GIMP plug-in for direct digital camera through gphoto2
Summary(pl.UTF-8):	Wtyczka GIMPa pozwalająca na dostęp do aparatów cyfrowych przez gphoto2
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	gimp >= 1:2.0

%description -n gimp-plugin-gtkam
GIMP plug-in for direct digital camera through gphoto2.

%description -n gimp-plugin-gtkam -l pl.UTF-8
Wtyczka GIMPa pozwalająca na dostęp do aparatów cyfrowych przez
gphoto2.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4 -I gphoto-m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_bonobo:--without-bonobo} \
	%{!?with_gnome:--without-gnome} \
	%{!?with_gimp:--without-gimp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/bin/scrollkeeper-update
%postun	-p /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/gtkam
%{_datadir}/%{name}
%{_mandir}/man1/gtkam.1*
%{_desktopdir}/gtkam.desktop
%{_pixmapsdir}/gtkam*.png

%if %{with gimp}
%files -n gimp-plugin-gtkam
%defattr(644,root,root,755)
%attr(755,root,root) %{gimpplugindir}/gtkam-gimp
%endif
