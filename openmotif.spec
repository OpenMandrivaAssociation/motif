%define intern_name openMotif
%define major 4
%define libname %mklibname %name %{major}
%define develname %mklibname %name -d

Summary: Open Motif runtime libraries and executables
Name: openmotif
Version: 2.3.2
Release: 2
License: Open Group Public License
Group: System/Libraries
Source:  %{name}-%{version}.tar.gz
Source1: xmbind
URL: http://www.motifzone.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires:	byacc pkgconfig
BuildRequires:	flex
BuildRequires:	libxp-devel
BuildRequires:	libxt-devel
BuildRequires:	libxft-devel
BuildRequires:	x11-data-bitmaps
BuildRequires:	libjpeg-devel libpng-devel
BuildRequires:	gcc-c++, gcc, gcc-cpp

Patch0: openMotif-2.3.0-no_demos.patch
Patch1: openMotif-2.2.3-uil_lib.patch
Patch2: openMotif-2.3.0-rgbtxt.patch
Patch3: openMotif-2.3.0-mwmrc_dir.patch
Patch4: openMotif-2.3.0-bindings.patch
Patch5: openMotif-2.3.0-no_X11R6.patch
Patch6: openMotif-2.3.0-fix-str-fmt.patch

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

%package -n %{develname}
Summary: Open Motif development libraries and header files
Group: Development/C
Conflicts: lesstif-devel <= 0.92.32-6
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}
Obsoletes: %{_lib}%{name}4-devel

%description -n %{develname}
This is the Open Motif %{version} development environment. It includes the
static libraries and header files necessary to build Motif applications.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .no_demos
%patch1 -p1 -b .uil_lib
%patch2 -p0 -b .rgbtxt
%patch3 -p0 -b .mwmrc_dir
%patch4 -p1 -b .bindings
%patch5 -p0 -b .no_X11R6
%patch6 -p1 -b .str-fmt

for i in doc/man/man3/{XmColumn,XmDataField}.3; do
	iconv -f windows-1252 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
export CC=gcc
export CXX=g++

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

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make DESTDIR=%{buildroot} prefix=%{prefix} install
mkdir -p %{buildroot}/etc/X11/xinit/xinitrc.d \
         %{buildroot}/usr/include

install -m 755 %{SOURCE1} %{buildroot}/etc/X11/xinit/xinitrc.d/xmbind.sh

rm -fr %{buildroot}%{prefix}/%{_lib}/*.la \
       %{buildroot}%{prefix}/share/Xm/doc


%files
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
%{_libdir}/libMrm.so.%{major}*
%{_libdir}/libUil.so.%{major}*
%{_libdir}/libXm.so.%{major}*

%files -n %{develname}
%{_bindir}/uil
%{prefix}/include/Mrm
%{prefix}/include/Xm
%{prefix}/include/uil
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_mandir}/man1/uil.1*
%{_mandir}/man3/*
%{_mandir}/man5/*


