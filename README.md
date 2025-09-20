# Waiting List x Landing Page

Switch quickly from a waiting list that feeds data to formbricks to a landing page.

Related Posts:

* https://jalcocert.github.io/JAlcocerT/how-to-create-a-waiting-list/

Adapt the MODE (waiting list or landing page) via the `.env` file: **Waiting list** or **landing page**

```sh
cp .env.example .env
#python3 porkbun-nameserver-manager.py 
```

*Optionally*:

* Configure [formbricks](https://formbricks.com/) form and questionaire
* Configure [Cloudflare](https://cloudflare.com/) DNS record via Python questionaire script `cloudflare-dns-updater.py`
* Get a domain from [Porkbun](https://porkbun.com/) via Python questionaire script `porkbun-domains.py`

See the website in action as per these makefile commands: *they spin up a local server and a production server*

```sh
#make help
make local-dev
#make local-prod

#make run-dev
make run-prod
```

**Forked from:**

* https://github.com/unoforge/agency-landing-page-Astrojs
* https://agencex-astro.vercel.app/#features

> MIT | A simple agency landing page made with astrojs and tailwindcss

---

<h1>AgenceX Landing page</h1>

A simple landing page for a digital agency

![AgenceX light Theme](./screens/demoLight.webp)
![AgenceX Dark Theme](./screens/demoDark.webp)


## Tools
- TailwindCSS v4
- AstroJs v5


## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```
/
├── public/
│   ├── images/
│   ├── logos/*
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── blocks/*
│   │   ├── cards/*
│   │   ├── elements/*
│   │   ├── sections/*
│   │   ├── shared/*
│   ├── layouts/
│   │   └── Layout.astro
│   └── pages/
│       └── index.astro
│   └── styles/
│       └── global.css
└── package.json
```


## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                | Action                                           |
| :--------------------- | :----------------------------------------------- |
| `npm install`          | Installs dependencies                            |
| `npm run dev`          | Starts local dev server at `localhost:4321`      |
| `npm run build`        | Build your production site to `./dist/`          |
| `npm run preview`      | Preview your build locally, before deploying     |
| `npm run astro ...`    | Run CLI commands like `astro add`, `astro check` |
| `npm run astro --help` | Get help using the Astro CLI                     |


