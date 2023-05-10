%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-lanelet2-examples
Version:        1.2.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS lanelet2_examples package

License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-humble-lanelet2-core
Requires:       ros-humble-lanelet2-io
Requires:       ros-humble-lanelet2-matching
Requires:       ros-humble-lanelet2-projection
Requires:       ros-humble-lanelet2-python
Requires:       ros-humble-lanelet2-routing
Requires:       ros-humble-lanelet2-traffic-rules
Requires:       ros-humble-mrt-cmake-modules
Requires:       ros-humble-ros2cli
Requires:       ros-humble-ros-workspace
BuildRequires:  ros-humble-ament-cmake-core
BuildRequires:  ros-humble-lanelet2-core
BuildRequires:  ros-humble-lanelet2-io
BuildRequires:  ros-humble-lanelet2-matching
BuildRequires:  ros-humble-lanelet2-projection
BuildRequires:  ros-humble-lanelet2-python
BuildRequires:  ros-humble-lanelet2-routing
BuildRequires:  ros-humble-lanelet2-traffic-rules
BuildRequires:  ros-humble-mrt-cmake-modules
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  gtest-devel
%endif

%description
Examples for working with Lanelet2

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Wed May 10 2023 Fabian Immel <fabian.immel@kit.edu> - 1.2.1-1
- Autogenerated by Bloom

* Tue Apr 19 2022 Fabian Poggenhans <fabian.poggenhans@kit.edu> - 1.1.1-4
- Autogenerated by Bloom

* Tue Feb 08 2022 Fabian Poggenhans <fabian.poggenhans@kit.edu> - 1.1.1-3
- Autogenerated by Bloom

