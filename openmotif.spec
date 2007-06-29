%define intern_name openMotif
%define major 3
%define libname %mklibname %name %major

Summary: Open Motif runtime libraries and executables
Name: openmotif
Version: 2.3.0
Release: %mkrel 1
License: Open Group Public License
Group: System/Libraries
Source:  %{name}-%{version}.tar.bz2
Source1: xmbind
URL: http://www.motifzone.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires:	byacc pkgconfig
BuildRequires:	flex
BuildRequires:	libxp-devel
BuildRequires:	libxt-devel
BuildRequires:	x11-data-bitmaps
BuildRequires:	libjpeg-devel libpng-devel

#Patch19: openMotif-2.2.3-utf8.patch
Patch22: openMotif-2.3.0-no_demos.patch
Patch23: openMotif-2.2.3-uil_lib.patch
#Patch25: openMotif-2.2.3-libdir.patch
#Patch26: openMotif-2.2.3-char_not_supported.patch
#Patch27: openMotif-2.2.3-pixel_length.patch
#Patch28: openMotif-2.2.3-popup_timeout.patch
#Patch29: openMotif-2.2.3-acinclude.patch
#Patch30: openMotif-2.2.3-autofoo.patch
#Patch31: openMotif-2.2.3-CAN-2004-0687-0688.patch
#Patch32: openMotif-2.2.3-CAN-2004-0914.patch
#Patch33: openMotif-2.2.3-CAN-2004-0914_autofoo.patch
#Patch34: openMotif-2.2.3-tmpnam.patch
#Patch35: openmotif-2.2.3-CAN-2004-0914_sec8.patch
#Patch36: openMotif-2.2.3-vizcount.patch
Patch37: openMotif-2.2.3-long64.patch
#Patch38: openMotif-2.2.3-multiscreen.patch
#Patch39: openMotif-2.2.3-motifzone_1193.patch
#Patch40: openMotif-2.2.3-motifzone_1202.patch
#Patch41: openMotif-2.2.3-CAN-2005-0605.patch
Patch43: openMotif-2.3.0-rgbtxt.patch
Patch45: openMotif-2.3.0-mwmrc_dir.patch
Patch46: openMotif-2.3.0-bindings.patch
Patch47: openMotif-2.3.0-no_X11R6.patch

Conflicts: lesstif <= 0.92.32-6

Prefix: /usr

%description
This is the Open Motif %{version} runtime environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif, and the Motif Window Manager "mwm".

%package -n %{libname}
Summary: Open Motif libraries
Group: System/Libraries
Provides: lib%{name} = %{version}-%{release}

%description -n %{libname}
These are the libraries provided by is the Open Motif %{version} runtime
environment. 

%package -n %{libname}-devel
Summary: Open Motif development libraries and header files
Group: Development/C
Conflicts: lesstif-devel <= 0.92.32-6
Provides: lib%{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}

%description -n %{libname}-devel
This is the Open Motif %{version} development environment. It includes the
static libraries and header files necessary to build Motif applications.

%prep
%setup -q -n %{name}-%{version}
#%patch19 -p1 -b .utf8
%patch22 -p0 -b .no_demos
%patch23 -p1 -b .uil_lib
#%patch25 -p1 -b .libdir
#%patch26 -p1 -b .char_not_supported
#%patch27 -p1 -b .pixel_length
#%patch28 -p1 -b .popup_timeout
#%patch29 -p1 -b .acinclude
#%patch30 -p1 -b .autofoo
#%patch31 -p1 -b .CAN-2004-0687-0688
#%patch32 -p1 -b .CAN-2004-0914
#%patch33 -p1 -b .CAN-2004-0914_autofoo
#%patch34 -p1 -b .tmpnam
#%patch35 -p1 -b .CAN-2004-0914_sec8
#%patch36 -p1 -b .vizcount
%patch37 -p1 -b .long64
#%patch38 -p1 -b .multiscreen
#%patch39 -p1 -b .motifzone_1193
#%patch40 -p1 -b .motifzone_1202
#%patch41 -p1 -b .CAN-2005-0605
%patch43 -p0 -b .rgbtxt
%patch45 -p0 -b .mwmrc_dir
%patch46 -p0 -b .bindings
%patch47 -p0 -b .no_X11R6

for i in doc/man/man3/{XmColumn,XmDataField}.3; do
	iconv -f windows-1252 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
./configure \
   --prefix=%{prefix} \
   --libdir=%{prefix}/%{_lib} \
   --enable-static

# do not use rpath
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make clean
make

%install
rm -rf $RPM_BUILD_ROOT

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make DESTDIR=$RPM_BUILD_ROOT prefix=%{prefix} install
mkdir -p $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d \
         $RPM_BUILD_ROOT/usr/include

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/xmbind.sh

mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share/man

rm -fr $RPM_BUILD_ROOT%{prefix}/%{_lib}/*.la \
       $RPM_BUILD_ROOT%{prefix}/share/Xm/doc

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYRIGHT.MOTIF README RELEASE RELNOTES
%{_sysconfdir}/X11/xinit/xinitrc.d/xmbind.sh
%{_sysconfdir}/X11/mwm/system.mwmrc
%{_bindir}/mwm
%{_bindir}/xmbind
%{prefix}/include/X11/bitmaps/*
%{_datadir}/X11/bindings
%{_mandir}/man1/mwm*
%{_mandir}/man1/xmbind*
%{_mandir}/man4/mwmrc*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libMrm.so.*
%{_libdir}/libUil.so.*
%{_libdir}/libXm.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/uil
%{prefix}/include/Mrm
%{prefix}/include/Xm
%{prefix}/include/uil
%{_libdir}
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_mandir}/man1/uil.1*
%{_mandir}/man3/*
%{_mandir}/man5/*


