#!/command/with-contenv bashio
# shellcheck shell=bash
# ==============================================================================
# Home Assistant Add-on: Qwackify
#
# Launch Caddy
# ------------------------------------------------------------------------------
prepare_caddy() {
    bashio::log.info 'Prepare Caddy...'

    # Set fixed Caddy binary path
    CADDY_PATH="/etc/caddy/caddy"
    export CADDY_PATH

    # Check for custom Caddy binary at fixed path
    if bashio::fs.file_exists "${CADDY_PATH}"; then
        bashio::log.info "Found custom Caddy at ${CADDY_PATH}"
        export CUSTOM_CADDY=true
    else
        export CUSTOM_CADDY=false
        bashio::log.info "Use built-in Caddy"
    fi

    # Check Caddy version
    "${CADDY_PATH}" version
}

caddy_upgrade() {
    bashio::log.info 'Upgrade Caddy...'

    if ! ${CUSTOM_CADDY}; then
        bashio::log.info "Cannot upgrade Caddy as no custom binary has been found"
        return 0
    elif ! [ -w ${CADDY_PATH} ]; then
        bashio::log.info "Custom Caddy has been found but is not writable"
        return 0
    elif [ "$(${CADDY_PATH} version | awk '{print $1}')" == "$(curl -sL https://api.github.com/repos/caddyserver/caddy/releases/latest | jq -r '.tag_name')" ]; then
        bashio::log.info "Custom Caddy uses the latest version"
        return 0
    else
        bashio::log.info "Initiate upgrade"
        "${CADDY_PATH}" upgrade
    fi
}

prepare_caddyfile() {
    bashio::log.info 'Prepare Caddyfile...'

    # Set fixed Caddyfile path
    CONFIG_PATH="/etc/caddy/Caddyfile"
    export CONFIG_PATH
    
    # Check for existing Caddyfile
    if bashio::fs.file_exists "${CONFIG_PATH}"; then
        bashio::log.info "Caddyfile found at ${CONFIG_PATH}"
        export CADDYFILE=true
    else
        bashio::log.info "No Caddyfile found"
        export CADDYFILE=false
    fi
}

caddy_fmt() {
    bashio::log.info 'Format Caddyfile...'

    if ! ${CADDYFILE}; then
        bashio::log.info "No Caddyfile found"
        return 0
    fi

    if [ -w ${CONFIG_PATH} ]; then
        bashio::log.info "Overwrite Caddyfile"
        "${CADDY_PATH}" fmt --overwrite ${CONFIG_PATH}
    else
        bashio::log.info "Caddyfile has been found but is not writable"
    fi
}

main() {
    bashio::log.trace "${FUNCNAME[0]}"

    declare name
    declare value
    declare -a args=()

    # Load command line arguments
    for arg in $(bashio::config 'args|keys'); do
        # shellcheck disable=SC2207
        args+=( $(bashio::config "args[${arg}]") )
    done

    # Load custom environment variables
    for var in $(bashio::config 'env_vars|keys'); do
        name=$(bashio::config "env_vars[${var}].name")
        value=$(bashio::config "env_vars[${var}].value")
        bashio::log.info "Setting ${name} to ${value}"
        export "${name}=${value}"
    done

    # Prepare Caddy
    prepare_caddy

    # Upgrade Caddy
    if bashio::config.true 'caddy_upgrade'; then
        caddy_upgrade
    fi

    # Prepare Caddyfile
    prepare_caddyfile

    # Format Caddyfile
    if bashio::config.true 'caddy_fmt'; then
        caddy_fmt
    fi

    # Run Caddy
    bashio::log.info "Run Caddy..."
    bashio::log.debug "'${CADDY_PATH}' run --config '${CONFIG_PATH}' '${args[*]}'"
    "${CADDY_PATH}" run --config "${CONFIG_PATH}" "${args[@]}"
}
main "$@"
