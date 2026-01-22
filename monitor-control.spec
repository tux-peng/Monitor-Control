Name:           monitor-control
Version:        1.0
Release:        1%{?dist}
Summary:        Monitor hardware control via DDC/CI
License:        MIT
URL:            https://github.com/tux-peng/Monitor-Control
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       ddcutil
Requires:       i2c-tools

%description
A set of Python tools to control monitor settings like brightness and 
contrast directly through hardware using the DDC/CI protocol.

# --- Subpackage: Qt ---
%package qt
Summary:        Monitor Control - PyQt6 Interface
Requires:       %{name} = %{version}-%{release}
Requires:       python-qt6-core

%description qt
A modern PyQt6 graphical interface for monitor hardware control.

# --- Subpackage: Tk ---
%package tk
Summary:        Monitor Control - Tkinter Interface
Requires:       %{name} = %{version}-%{release}
Requires:       tkinter

%description tk
A lightweight, zero-dependency Tkinter interface for monitor control.

%prep
%autosetup -n Monitor-Control-%{version}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/pixmaps

# Install executable scripts
install -m 755 monitor_control_qt.py %{buildroot}%{_bindir}/monitor-control-qt
install -m 755 monitor_control_tk.py %{buildroot}%{_bindir}/monitor-control-tk

# Install common assets
install -m 644 monitor_control.png %{buildroot}%{_datadir}/pixmaps/monitor-control.png

# Install desktop entries
install -m 644 monitor-control-qt.desktop %{buildroot}%{_datadir}/applications/
install -m 644 monitor-control-tk.desktop %{buildroot}%{_datadir}/applications/

%files
%{_datadir}/pixmaps/monitor-control.png
# Add a LICENSE file to your repo to satisfy this:
# %license LICENSE 

%files qt
%{_bindir}/monitor-control-qt
%{_datadir}/applications/monitor-control-qt.desktop

%files tk
%{_bindir}/monitor-control-tk
%{_datadir}/applications/monitor-control-tk.desktop

%post
# Post-install message for group permissions
echo "To use these tools without sudo, add your user to the i2c group:"
echo "sudo usermod -aG i2c $USER"

%changelog
* Wed Jan 21 2026 tux-peng - 1.0-1
- Initial release with Qt and Tk subpackages
