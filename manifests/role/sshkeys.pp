# Deploys SSH authorized keys from an arbitrary number of ssh::authorized_keys
# style hashes (either in global (default) or the ssh::keys:: name space).
class base::role::sshkeys (
  $key_sources = hiera('ssh::key_sources', ['ssh::keys']),
) {
    $keys_merged = merge_hiera_hashes($key_sources)

    class { 'base::profile::ssh::authorized_keys':
      authorized_keys => $keys_merged,
      }
}
