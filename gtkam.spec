#
# Conditional build:
%bcond_without	bonobo	# don't use bonobo
%bcond_without	gnome	# don't use GNOME to display documentation
%bcond_without	gimp	# don't build GIMP plugin
#
Summary:	GTKam - graphical frontend for gphoto2
Summary(pl):	GTKam - graficzny interfejs do gphoto2
Name:		gtkam
Version:	0.1.11
Release:	1
License:	LGPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/gphoto/%{name}-%{version}.tar.gz
# Source0-md5:	084e90e73179e9cac6664fd1b30e86d8
Patch0:		%{name}-paths.patch
Patch1:		%{name}-gimp2.patch
Patch2:		%{name}-locale-names.patch
Patch3:		%{name}-enable_deprecated.patch
Patch4:		%{name}-gnome_help_path.patch
URL:		http://www.gphoto.org/proj/gtkam/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_bonobo:BuildRequires:	bonobo-activation-devel}
%{?with_gimp:BuildRequires:	gimp-devel >= 1:2.0}
BuildRequires:	gnome-common
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
%{?with_bonobo:BuildRequires:	libbonoboui-devel}
BuildRequires:	libexif-gtk-devel >= 0.3.2
%{?with_gnome:BuildRequires:	libgnomeui-devel}
BuildRequires:	libgphoto2-devel >= 2.1.4
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	scrollkeeper
Requires:	libgphoto2 >= 2.1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with gimp}
%define		gimpplugindir	%(gimptool --gimpplugindir)/plug-ins
%endif

%description
The gtkam package provides a gtk-based frontend to gphoto2.

%description -l pl
Pakiet gtkam udostêpnia oparty o gtk graficzny interfejs do gphoto2.

%package -n gimp-plugin-gtkam
Summary:	GIMP plug-in for direct digital camera through gphoto2
Summary(pl):	Wtyczka GIMPa pozwalaj±ca na dostêp do aparatów cyfrowych przez gphoto2
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	gimp >= 1:2.0

%description -n gimp-plugin-gtkam
GIMP plug-in for direct digital camera through gphoto2.

%description -n gimp-plugin-gtkam -l pl
Wtyczka GIMPa pozwalaj±ca na dostêp do aparatów cyfrowych przez
gphoto2.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

mv po/{no,nb}.po

%build
rm -f missing
intltoolize --copy --force
glib-gettextize --copy --force
gnome-doc-common --copy
%{__libtoolize}
%{__aclocal}
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

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /usr/bin/scrollkeeper-update
%postun -p /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_omf_dest_dir}/%{name}

%if %{with gimp}
%files -n gimp-plugin-gtkam
%defattr(644,root,root,755)
%attr(755,root,root) %{gimpplugindir}/gtkam-gimp
%endif
