%define major 4
%define libname %mklibname xm %{major}
%define mrmlibname %mklibname mrm %{major}
%define uillibname %mklibname uil %{major}
%define develname %mklibname %name -d

Summary: Open Motif runtime libraries and executables
Name: motif
Version: 2.3.4
Release: 1
License: LGPLv2+
Group: System/Libraries
Source0: http://sourceforge.net/projects/motif/files/motif-%{version}-src.tgz
Source1: xmbind
URL: http://motif.ics.com/

BuildRequires:	byacc pkgconfig
BuildRequires:	flex
BuildRequires:	libxt-devel
BuildRequires:	libxft-devel
BuildRequires:	x11-data-bitmaps
BuildRequires:	jpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	gcc-c++, gcc, gcc-cpp

Patch0: openMotif-2.3.0-no_demos.patch
Patch1: openMotif-2.2.3-uil_lib.patch
Patch2: openMotif-2.3.0-rgbtxt.patch
Patch3: openMotif-2.3.0-mwmrc_dir.patch
Patch4: openMotif-2.3.0-bindings.patch
Patch5: openMotif-2.3.0-no_X11R6.patch
Patch6: openMotif-2.3.0-fix-str-fmt.patch
Patch7: openmotif-2.3.3-automake-1.13.patch
Patch8: openmotif-2.3.3-jpeg.patch
Patch9: motif-2.3.4-freetype-fontconfig.patch

Conflicts: lesstif <= 0.92.32-6

%description
This is the Open Motif %{version} runtime environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif, and the Motif Window Manager "mwm".

%package -n %{libname}
Summary: Main Motif library
Group: System/Libraries

%description -n %{libname}
This is the main Motif widget toolkit runtime library.

%package -n %{mrmlibname}
Summary: The Motif widget fetching library
Group: System/Libraries

%description -n %{mrmlibname}
This is the Motif library used for fetching widgets from UIL.

%package -n %{uillibname}
Summary: The Motif User Interface Langage runtime library
Group: System/Libraries

%description -n %{uillibname}
This library can be used to handle Motif UIL source files.

%package -n %{develname}
Summary: Motif development libraries and header files
Group: Development/C
Conflicts: lesstif-devel <= 0.92.32-6
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}
Requires: %{mrmlibname} = %{version}-%{release}
Requires: %{uillibname} = %{version}-%{release}
Obsoletes: %{_lib}%{name}4-devel

%description -n %{develname}
This is the Motif %{version} development environment. It includes the
static libraries and header files necessary to build Motif applications.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .no_demos
%patch1 -p1 -b .uil_lib
%patch2 -p0 -b .rgbtxt
%patch3 -p1 -b .mwmrc_dir
%patch4 -p1 -b .bindings
%patch5 -p0 -b .no_X11R6
%patch6 -p1 -b .str-fmt
%patch7 -p1 -b .am113
%patch8 -p1
%patch9 -p1

for i in doc/man/man3/{XmColumn,XmDataField}.3; do
	iconv -f windows-1252 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
export CC=gcc
export CXX=g++

libtoolize --copy --force --install
aclocal -I.
autoheader
automake -a -c -f --foreign
autoconf

CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
%configure2_5x \
   --enable-static

# do not use rpath
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool

make clean
%make

%install

%makeinstall_std
mkdir -p %{buildroot}/etc/X11/xinit/xinitrc.d \
         %{buildroot}/usr/include

install -m 755 %{SOURCE1} %{buildroot}/etc/X11/xinit/xinitrc.d/xmbind.sh

rm -fr %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_datadir}/Xm/doc


%files
%doc COPYING README RELEASE RELNOTES
%{_sysconfdir}/X11/xinit/xinitrc.d/xmbind.sh
%{_sysconfdir}/X11/mwm/system.mwmrc
%{_bindir}/mwm
%{_bindir}/xmbind
%{_includedir}/X11/bitmaps/*
%{_datadir}/X11/bindings
%{_mandir}/man1/mwm*
%{_mandir}/man1/xmbind*
%{_mandir}/man4/mwmrc*

%files -n %{libname}
%{_libdir}/libXm.so.%{major}*

%files -n %{mrmlibname}
%{_libdir}/libMrm.so.%{major}*

%files -n %{uillibname}
%{_libdir}/libUil.so.%{major}*

%files -n %{develname}
%{_bindir}/uil
%{_includedir}/Mrm
%{_includedir}/Xm
%{_includedir}/uil
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_mandir}/man1/uil.1*
%{_mandir}/man3/*
%{_mandir}/man5/*


