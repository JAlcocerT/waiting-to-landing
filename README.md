# Waiting List x Landing Page

Adapt the MODE (waiting list or landing page) via the .env file

``sh
cp .env.example .env
```

*Optionally*:

* Configure formbricks form and questionaire
* Configure Cloudflare DNS record via Python questionaire script
* Get a domain from Porkbun via Python questionaire script

See the website in action as per:

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


