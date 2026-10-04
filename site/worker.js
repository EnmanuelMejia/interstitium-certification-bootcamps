/* Cert-Bootcamps edge router (main_module).
   Routes: <host>/bootcamps/* -> this worker. Static assets live at the site
   root, so strip the /bootcamps prefix and delegate to the asset manifest. */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/bootcamps" || url.pathname.startsWith("/bootcamps/")) {
      const rest = url.pathname.slice("/bootcamps".length) || "/";
      url.pathname = rest;
      return env.ASSETS.fetch(new Request(url.toString(), request));
    }
    return env.ASSETS.fetch(request);
  }
};
