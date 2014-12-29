# -*- mode: ruby -*-
# # vi: set ft=ruby :

Vagrant.require_version ">= 1.6.0"

ETCD_DISCOVERY_URL = `curl -s https://discovery.etcd.io/new`
CLOUD_CONFIG_DATA = <<-CLOUD
#cloud-config

coreos:
  etcd:
    discovery: #{ETCD_DISCOVERY_URL}
    addr: $public_ipv4:4001
    peer-addr: $public_ipv4:7001
  units:
    - name: etcd.service
      command: start
    - name: docker-tcp.socket
      command: start
      enable: yes
      content: |
        [Unit]
        Description=Docker Socket for the API

        [Socket]
        ListenStream=2375
        BindIPv6Only=both
        Service=docker.service

        [Install]
        WantedBy=sockets.target
    - name: enable-docker-tcp.service
      command: start
      content: |
        [Unit]
        Description=Enable the Docker Socket for the API

        [Service]
        Type=oneshot
        ExecStart=/usr/bin/systemctl enable docker-tcp.socket
CLOUD

# Defaults
$num_instances = 3
$update_channel = "stable"
$enable_serial_logging = false
$vb_gui = false
$vb_memory = 1024
$vb_cpus = 1

# Attempt to apply the deprecated environment variable NUM_INSTANCES to
# $num_instances while allowing config.rb to override it
if ENV["NUM_INSTANCES"].to_i > 0 && ENV["NUM_INSTANCES"]
  $num_instances = ENV["NUM_INSTANCES"].to_i
end

Vagrant.configure("2") do |config|
  config.vm.box = "coreos-%s" % $update_channel
  config.vm.box_version = ">= 308.0.1"
  config.vm.box_url = "http://%s.release.core-os.net/amd64-usr/current/coreos_production_vagrant.json" % $update_channel

  # Newer Vagrant tries to replace the default SSH key and CoreOS filesystems
  # are not persistent, so always use the insecure key instead.
  config.ssh.insert_key = false

  # CoreOS doesn't come with a /etc/hosts file. To get the vagrant-hostmanager
  # plugin working, we need a hosts file to first download and check.
  config.vm.provision "shell", inline: "touch /etc/hosts"

  config.vm.provider :virtualbox do |v|
    # On VirtualBox, we don't have guest additions or a functional vboxsf
    # in CoreOS, so tell Vagrant that so it can be smarter.
    v.check_guest_additions = false
    v.functional_vboxsf     = false
  end

  # plugin conflict
  if Vagrant.has_plugin?("vagrant-vbguest") then
    config.vbguest.auto_update = false
  end

  if Vagrant.has_plugin?("vagrant-hostmanager") then
    # Disable vagrant-hostmanager plugin so we can run it as a provisioner instead.
    config.hostmanager.enabled = false
    config.hostmanager.include_offline = true
  end

  # This runs the vagrant-hostmanager provisioner after the shell one above so
  # our /etc/hosts file is already in place.
  config.vm.provision :hostmanager

  (1..$num_instances).each do |i|
    config.vm.define vm_name = "core%02d" % i do |config|
      config.vm.hostname = vm_name

      config.vm.network "forwarded_port", guest: 2375, host: (2375 + i - 1), auto_correct: true

      config.vm.provider :virtualbox do |vb|
        vb.gui = $vb_gui
        vb.memory = $vb_memory
        vb.cpus = $vb_cpus
      end

      config.vm.network :private_network, ip: "172.17.8.#{i+100}"

      if not CLOUD_CONFIG_DATA.nil?
        config.vm.provision :shell, :inline => "echo '#{CLOUD_CONFIG_DATA}' > /tmp/vagrantfile-user-data"
        config.vm.provision :shell, :inline => "mv /tmp/vagrantfile-user-data /var/lib/coreos-vagrant/", :privileged => true
      end

    end
  end
end
