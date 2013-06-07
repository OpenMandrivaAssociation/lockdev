%define	major 1
%define libname %mklibname lockdev %{major}
%define devname %mklibname lockdev -d

%define _with_perl 0

# Where lock files are stored
%global _lockdir /run/lock/lockdev

%global checkout 20111007git
%global co_date  2011-10-07

Summary:	A library for locking devices
Name:		lockdev
Version:	1.0.4
Release:	1.%{checkout}.2
License:	LGPLv2
Group:		System/Libraries
Url:		ftp://ftp.debian.org/debian/pool/main/l/lockdev/
# This is a nightly snapshot downloaded via
# https://alioth.debian.org/snapshots.php?group_id=100443
Source0:	lockdev-%{version}.%{checkout}.tar.gz
BuildRequires:	chrpath
%if %_with_perl
BuildRequires:	perl-devel
%endif
Requires(pre):	rpm-helper

%description
Lockdev provides a reliable way to put an exclusive lock to devices using both
FSSTND and SVr4 methods.

%package -n	%{libname}
Summary:	A library for locking devices
Group:		System/Libraries

%description -n	%{libname}
Lockdev provides a reliable way to put an exclusive lock to devices using both
FSSTND and SVr4 methods.

%package -n	%{devname}
Summary:	The development library and header files for the lockdev library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}lockdev1-devel < 1.0.4-0.120111007git.8

%description -n	%{devname}
The lockdev library provides a reliable way to put an exclusive lock on devices
using both FSSTND and SVr4 methods. The lockdev-devel package contains the
development library and headers.

%if %_with_perl
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
%endif

%prep
%setup -qn lockdev-scm-%{co_date}

%build
# Generate version information from git release tag
./scripts/git-version > VERSION

# To satisfy automake
touch ChangeLog
mkdir -p m4

# Bootstrap autotools
autoreconf --verbose --force --install

CFLAGS="%{optflags} -D_PATH_LOCK=\\\"%{_lockdir}\\\"" \
%configure 2_5 \
	--disable-static \
	--enable-helper

%make

%if %_with_perl
pushd LockDev
    perl Makefile.PL INSTALLDIRS=vendor
    make OPTIMIZE="%{optflags}"
popd
%endif

%install
# Fix upstream permission bug #3053
chmod 644 docs/LSB.991201
%makeinstall_std

%pre
getent group lock >/dev/null || groupadd -g 54 -r -f lock
exit 0

%if %_with_perl
# nuke rpath
chrpath -d %{buildroot}%{perl_vendorarch}/auto/LockDev/*.so
%endif

%files
%doc AUTHORS ChangeLog ChangeLog.old README.debug docs/LSB.991201
%attr(2755,root,lock) %{_sbindir}/lockdev
%{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/liblockdev.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*.h
%{_mandir}/man3/lockdev.3*
%{_libdir}/pkgconfig/lockdev.pc

%if %_with_perl
%files -n perl-LockDev
%{perl_vendorarch}/LockDev.pm
%dir %{perl_vendorarch}/auto/LockDev
%attr(0755,root,root) %{perl_vendorarch}/auto/LockDev/*.so
%{_mandir}/man3/LockDev.3*
%endif
