%define	major 1
%define libname	%mklibname lockdev %{major}

Summary:	A library for locking devices
Name:		lockdev
Version:	1.0.3
Release:	%mkrel 4
License:	LGPL
Group:		System/Libraries
URL:		ftp://ftp.debian.org/debian/pool/main/l/lockdev/
Source0:	ftp://ftp.debian.org/debian/pool/main/l/lockdev/%{name}_%{version}.orig.tar.bz2
# (blino) rediffed for 1.0.3, from 1.0.0 RH patch
Patch0:		lockdev-1.0.3-rh.patch
Patch1:		lockdev-1.0.0-shared.patch
Patch2:		lockdev-1.0.0-signal.patch
Patch3:		lockdev-1.0.0-cli.patch
# merged upstream
#Patch4:	lockdev-1.0.1-checkname.patch
# (blino) rediffed for 1.0.3, from 1.0.1 RH patch
Patch5:		lockdev-1.0.3-pidexists.patch
# upstream has a similar workaround (with ':' instead of pppd-like '_' to replace '/')
#Patch6:	lockdev-1.0.1-subdir.patch
Patch7:		lockdev-1.0.1-fcntl.patch
# (blino) rediffed for 1.0.3, from 1.0.1 RH patch
Patch8:		lockdev-1.0.3-32bit.patch
Patch10:	lockdev-1.0.3-perlmake.patch
# (blino) link lockdev helper with shared library (from PLD)
Patch11:	lockdev-1.0.3-shared2.patch
BuildRequires:	chrpath perl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Lockdev provides a reliable way to put an exclusive lock to devices using both
FSSTND and SVr4 methods.

%package -n	%{libname}
Summary:	A library for locking devices
Group:		System/Libraries
Requires:	%{name}-baudboy

%description -n	%{libname}
Lockdev provides a reliable way to put an exclusive lock to devices using both
FSSTND and SVr4 methods.

%package -n	%{libname}-devel
Summary:	The Static lockdev library and header files for the lockdev library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
The lockdev library provides a reliable way to put an exclusive lock on devices
using both FSSTND and SVr4 methods. The lockdev-devel package contains the
static development library and headers.

%package	baudboy
Summary:	Lockdev utility
Group:		System/Kernel and hardware
Requires:	%{libname} = %{version}-%{release}

%description	baudboy
This package contains sgid lockdev utility used by Baudboy API.

%package -n	perl-LockDev
Summary:	LockDev - Perl extension to manage device lockfiles
Group:		Development/Perl
Requires:	%{libname} = %{version}-%{release}

%description -n	perl-LockDev
The LockDev methods act on device locks normally located in /var/lock. The lock
is acquired creating a pair of files hardlinked between them and named after
the device name (as mandated by FSSTND) and the device's major and minor
numbers (as in SVr4 locks). This permits to circumvent a problem using only the
FSSTND lock method when the same device exists under different names (for
convenience or when a device must be accessible by more than one group of
users).

The lock file names are typically in the form LCK..ttyS1 and LCK.004.065, and
their content is the pid of the process who owns the lock.

%prep

%setup -q
%patch0 -p1 -b .redhat
%patch1 -p1 -b .shared
%patch2 -p1 -b .signal
%patch3 -p1 -b .jbj
#%patch4 -p1 -b .checkname
%patch5 -p1 -b .pidexists
#%patch6 -p1 -b .subdir
%patch7 -p1 -b .fcntl
%patch8 -p1 -b .32bit
%patch10 -p1 -b .perlmake
%patch11 -p1 -b .shared2

%build

make shared static lockdev CC="%{__cc}" CFLAGS="%{optflags}"

pushd LockDev
    perl Makefile.PL INSTALLDIRS=vendor
    make OPTIMIZE="%{optflags}"
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_mandir}/man3

install -m0755 liblockdev.so.1.0.3 %{buildroot}%{_libdir}/
ln -snf liblockdev.so.1.0.3 %{buildroot}%{_libdir}/liblockdev.so.1
ln -snf liblockdev.so.1.0.3 %{buildroot}%{_libdir}/liblockdev.so

install -m0644 liblockdev.a %{buildroot}%{_libdir}/
install -m0644 src/*.h %{buildroot}%{_includedir}/
install -m0755 lockdev %{buildroot}%{_sbindir}/
install -m0644 docs/lockdev.3 %{buildroot}%{_mandir}/man3/

%makeinstall_std -C LockDev

# nuke rpath
chrpath -d %{buildroot}%{perl_vendorarch}/auto/LockDev/*.so

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog ChangeLog.old LICENSE README.debug docs/LSB.991201
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_mandir}/man3/lockdev.3*

%files baudboy
%defattr(-,root,root)
%attr(2755,root,uucp) %{_sbindir}/lockdev

%files -n perl-LockDev
%defattr(-,root,root)
%{perl_vendorarch}/LockDev.pm
%dir %{perl_vendorarch}/auto/LockDev
%attr(0755,root,root) %{perl_vendorarch}/auto/LockDev/*.so
%{_mandir}/man3/LockDev.3*
