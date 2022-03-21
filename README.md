Python 3.9.10
pip install django==3.2
pip install psycopg2-binary==2.8.6 (versiones más actuales dan problemas por el formateo UTC)
Instalación y configuración de tailwind
cmd - npm install -D tailwindcss postcss  postcss postcss-cli autoprefixer
cmd - npx tailwindcss init


f tailwind.config.js
	module.exports = {
 	 content: ["./app/templates/app/*.{html,js}"],
	  theme: {
	    extend: {},
	  },
	  plugins: [],
	}


f -(create) postcss.config.js
	module.exports = {
		plugins: {
			tailwindcss: {},
			autoprefixer: {}
		}
	}
	
	
d - static/css/*.css
	@tailwind base;
	@tailwind components;
	@tailwind utilities;


f - package.json
	{
	  "scripts":{
		"build":"postcss static/css/styles.css -o static/css/styles.min.css"   ### Este es el que hay que escribir, el resto se genera automáticamente -> indicas ruta del css y donde y con que nombre se minimiza
	  },
	  "devDependencies": {
		"autoprefixer": "^10.4.4",
		"postcss": "^8.4.12",
		"postcss-cli": "^9.1.0",
		"tailwindcss": "^3.0.23"
	  }
	}

cmd - npm run build

f - (create) templates/app/*.html
	<link href="{% static 'css/styles.min.css' %}" rel="stylesheet">  #Indicar la ruta del css minimizado