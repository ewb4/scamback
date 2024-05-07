Summary:        E-Mail BackScatter prevention using Sendmail's Milter interface
Name:           scamback
Version:        1.5.1
Release:        1%{?dist}
License:        Eland Systems
URL:            http://www.elandsys.com/scam/scam-backscatter/
Source0:        http://www.elandsys.com/scam/scam-backscatter/%{name}-%{version}.tgz
Source1:        scam-back-tmpfilesdir.conf
Source2:        scam-back.service
Source3:        scam-back-sysconfig
Source4:        scam-back-moredocs.tar.gz
Source5:        milterconfig.html
Source6:        scam-back-wrapper
Patch0:         rc.scamback.1.3.patch
BuildRequires:  gcc
BuildRequires:  make
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  sendmail-milter-devel >= 8.12.0
BuildRequires:  systemd-rpm-macros
%else
BuildRequires:  sendmail-devel >= 8.12.0
BuildRequires:  systemd
%endif
%{?systemd_requires}
Requires(pre):  shadow-utils
Requires:       sendmail-cf
Requires:       sendmail-milter

%description
Scam-backscatter prevents backscatter (accept and bounce) on mail servers
which don't host mailboxes locally. It validates mailboxes by verifying
the recipient addresses hosted on a different mail server.

%prep

%setup -q -n %{name}
%setup -q -n %{name} -a 4
cp -pf Makefile.linux Makefile
cp -pf scam.conf scam.conf.example

%build
CCFLAGS="-DUSEMAILERTABLE -g" make

%install
install -D -p -m 755 scam-back $RPM_BUILD_ROOT%{_bindir}/scam-back
install -D -p -m 644 scam.conf $RPM_BUILD_ROOT%{_sysconfdir}/mail/scam.conf
install -D -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_tmpfilesdir}/scam-back.conf
install -D -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/scam-back
#install -d -m 0755 %{buildroot}/run/scam-back

# Install systemd unit files and tmpfiles
##install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/scam-back.service
##install -D -p -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/%{name}-wrapper
install -D -p -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/scam-back-wrapper

%pre
getent group smmsp > /dev/null || %{_sbindir}/groupadd -r smmsp
getent passwd scamback > /dev/null || %{_sbindir}/useradd -r -g smmsp -d %{_localstatedir}/spool/scamback -s /sbin/nologin -c "scam-backscatter User" scamback
exit 0

%post
##%systemd_post %{name}.service
%systemd_post scam-back.service

%preun
##%systemd_preun %{name}.service
%systemd_preun scam-back.service

%postun
##%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart scam-back.service

%files
%license License
%doc INSTALL
%doc README
%doc CHANGES
%doc scam.conf.example
# Gleaned from http://www.sendmail.org/~gshapiro/8.10.Training/milterconfig.html
%doc milterconfig.html
%{_bindir}/*
##%{_libexecdir}/%{name}-wrapper
%{_libexecdir}/scam-back-wrapper
%{_tmpfilesdir}/scam-back.conf
%config(noreplace) %{_sysconfdir}/mail/scam.conf
%config(noreplace) %{_sysconfdir}/sysconfig/scam-back
##%{_unitdir}/%{name}.service
%{_unitdir}/scam-back.service

%changelog
* Thu Jul 28 2022 E. Wes Brown <EWBr0wn on GitHub.com> 1.5.1-1
- Initial spec file