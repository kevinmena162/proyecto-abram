import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from authors.models import Author, Post, Comment

class Command(BaseCommand):
    help = "Pobla la base de datos con los perfiles e información de los 5 autores de la psicología/administración."

    def handle(self, *args, **options):
        self.stdout.write("Eliminando datos existentes...")
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Author.objects.all().delete()

        self.stdout.write("Creando autores...")

        # 1. Abraham Maslow
        maslow = Author.objects.create(
            name="Abraham Maslow",
            username="abraham_maslow",
            occupation="Psicólogo Humanista",
            bio="Creador de la Jerarquía de Necesidades. Defensor del potencial humano y de la autorrealización como motivación fundamental. 🧠🌱",
            followers_count=124000,
            following_count=82,
            birth_info="1 de abril de 1908, Brooklyn, Nueva York, EE. UU.",
            death_info="8 de junio de 1970, Menlo Park, California, EE. UU.",
            nationality="Estadounidense",
            website="https://www.maslow-institute.org",
            key_theories="**Teoría de la Motivación Humana (Pirámide de Maslow)**:\nEstablece una jerarquía de necesidades humanas donde las necesidades básicas inferiores (fisiológicas, seguridad, afiliación, reconocimiento) deben ser satisfechas antes de que una persona pueda aspirar a la autorrealización, que es el desarrollo máximo del potencial personal.",
            academic_background="Cursó estudios de leyes en el City College of New York (CCNY) antes de trasladarse a la Universidad de Wisconsin, donde obtuvo su doctorado en Psicología en 1934. Fue profesor en el Brooklyn College y posteriormente director del departamento de psicología en la Universidad de Brandeis.",
            legacy="Es el principal exponente de la **Psicología Humanista** (la 'Tercera Fuerza'), que reaccionó contra el psicoanálisis freudiano y el conductismo de Skinner. Su pirámide sigue siendo un pilar fundamental en administración de empresas (recursos humanos), educación y coaching personal."
        )
        self.assign_profile_picture(maslow, "maslow.png")

        # 2. B. F. Skinner
        skinner = Author.objects.create(
            name="B. F. Skinner",
            username="bf_skinner",
            occupation="Psicólogo Conductista",
            bio="Defensor del conductismo radical. Creador del condicionamiento operante y la caja de Skinner. Todo comportamiento es moldeado por consecuencias. 🐁⚡",
            followers_count=98500,
            following_count=45,
            birth_info="20 de marzo de 1904, Susquehanna, Pensilvania, EE. UU.",
            death_info="18 de agosto de 1990, Cambridge, Massachusetts, EE. UU.",
            nationality="Estadounidense",
            website="https://www.bfskinner.org",
            key_theories="**Condicionamiento Operante y Conductismo Radical**:\nExplicó que la conducta humana no depende de variables internas inobservables (como la mente o el alma), sino del aprendizaje resultante de las consecuencias de la acción. Introdujo conceptos clave como **Refuerzo Positivo** (premiar conducta), **Refuerzo Negativo** (retirar estímulo aversivo), **Castigo** y **Extinción**.",
            academic_background="Graduado inicialmente en Literatura Inglesa en Hamilton College. Posteriormente obtuvo su doctorado en Psicología en la Universidad de Harvard en 1931. Dedicó su carrera académica a la investigación en la Universidad de Minnesota, la Universidad de Indiana y finalmente regresó a Harvard como profesor emérito.",
            legacy="Considerado el psicólogo más influyente del siglo XX. Sus hallazgos transformaron la educación a través de la instrucción programada, impulsaron la terapia cognitivo-conductual actual, dieron herramientas fundamentales para el entrenamiento animal y propusieron utopías sociales basadas en el diseño ambiental (como en su novela 'Walden Dos')."
        )
        self.assign_profile_picture(skinner, "skinner.png")

        # 3. Douglas McGregor
        mcgregor = Author.objects.create(
            name="Douglas McGregor",
            username="douglas_mcgregor",
            occupation="Teórico de la Administración",
            bio="Creador de la Teoría X y Teoría Y sobre la gestión y el liderazgo organizacional. Profesor distinguido en el MIT. 👔🤝",
            followers_count=75300,
            following_count=92,
            birth_info="16 de septiembre de 1906, Detroit, Míchigan, EE. UU.",
            death_info="1 de octubre de 1964, Massachusetts, EE. UU.",
            nationality="Estadounidense",
            website="https://sloan.mit.edu",
            key_theories="**Teoría X y Teoría Y**:\nSon dos conjuntos de supuestos sobre la naturaleza del trabajador humano:\n- **Teoría X**: Asume que los empleados son perezosos por naturaleza, evitan responsabilidades y deben ser controlados, dirigidos y amenazados con castigos para lograr metas.\n- **Teoría Y**: Supone que los empleados ven el trabajo como algo natural, son creativos, buscan responsabilidades y se automotivan cuando están comprometidos con los objetivos organizacionales.",
            academic_background="Se graduó de Wayne State University y luego obtuvo su doctorado en Psicología Experimental en la Universidad de Harvard en 1935. Fungió como presidente del Antioch College (1948-1954) y fue profesor titular de Administración Industrial en la Sloan School of Management del MIT.",
            legacy="Redefinió los recursos humanos y la teoría organizacional moderna. Al proponer que el estilo de liderazgo depende de las creencias que el líder tiene sobre sus empleados, promovió un modelo de administración participativo y humanista en contraposición al control taylorista tradicional."
        )
        self.assign_profile_picture(mcgregor, "mcgregor.png")

        # 4. Victor Vroom
        vroom = Author.objects.create(
            name="Victor Vroom",
            username="victor_vroom",
            occupation="Profesor de Psicología y Liderazgo",
            bio="Padre de la Teoría de las Expectativas de la motivación y experto en toma de decisiones gerenciales. Profesor emérito en Yale. 📊🧠",
            followers_count=56100,
            following_count=110,
            birth_info="9 de agosto de 1932, Montreal, Quebec, Canadá",
            death_info="Vive en Connecticut, EE. UU. (Edad actual: 93 años)",
            nationality="Canadiense-Estadounidense",
            website="https://som.yale.edu/faculty/victor-vroom",
            key_theories="**Teoría de las Expectativas (Fórmula de Motivación Vroom)**:\nPropone que la motivación del trabajador es un proceso cognitivo racional determinado por tres factores:\n- **Expectativa (E)**: La creencia de que el esfuerzo conducirá a un desempeño exitoso.\n- **Instrumentalidad (I)**: La creencia de que el desempeño exitoso será recompensado.\n- **Valencia (V)**: El valor personal que el empleado le asigna a la recompensa.\n*Fórmula: Motivación = Expectativa x Instrumentalidad x Valencia (M = E * I * V)*",
            academic_background="Obtuvo su licenciatura en artes de la Universidad McGill en Montreal, y su doctorado en Psicología Industrial y Organizacional en la Universidad de Michigan. Impartió clases en Carnegie Mellon University y la Universidad de Rochester antes de integrarse a la Yale School of Management.",
            legacy="Aportó un marco cognitivo y analítico riguroso a la motivación de los empleados, permitiendo a los directivos diseñar planes de incentivos personalizados y transparentes. Desarrolló además el modelo Vroom-Yetton de liderazgo situacional para optimizar la toma de decisiones."
        )
        self.assign_profile_picture(vroom, "vroom.png")

        # 5. Frederick Herzberg
        herzberg = Author.objects.create(
            name="Frederick Herzberg",
            username="frederick_herzberg",
            occupation="Psicólogo del Trabajo y las Organizaciones",
            bio="Creador de la Teoría de los Dos Factores (Motivación e Higiene). Pionero del enriquecimiento del trabajo laboral. 💼✨",
            followers_count=88200,
            following_count=61,
            birth_info="18 de abril de 1923, Lynn, Massachusetts, EE. UU.",
            death_info="19 de enero de 2000, Salt Lake City, Utah, EE. UU.",
            nationality="Estadounidense",
            website="https://www.hbr.org",
            key_theories="**Teoría de los Dos Factores (Motivación e Higiene)**:\nPostula que existen dos conjuntos independientes de factores que afectan la satisfacción laboral:\n- **Factores de Higiene (Extrínsecos)**: Su presencia no motiva, pero su ausencia causa insatisfacción profunda (sueldo, políticas de empresa, condiciones físicas, relaciones). \n- **Factores de Motivación (Intrínsecos)**: Generan satisfacción y compromiso real (logros, reconocimiento, el trabajo mismo, responsabilidad, crecimiento personal).",
            academic_background="Cursó sus estudios superiores en el City College de Nueva York. Posteriormente se alistó en el ejército durante la Segunda Guerra Mundial, sirviendo como sargento de patrulla médica y presenciando la liberación de Dachau. Al volver de la guerra, obtuvo su maestría y doctorado en la Universidad de Pittsburgh.",
            legacy="Herzberg popularizó el concepto de **Enriquecimiento del Trabajo** (job enrichment) para diseñar puestos de trabajo con tareas variadas y autónomas. Su artículo de 1968 en Harvard Business Review, *'One More Time: How Do You Motivate Employees?'*, es uno de los más vendidos en la historia de la publicación."
        )
        self.assign_profile_picture(herzberg, "herzberg.png")

        self.stdout.write("Creando publicaciones...")

        # --- POSTS DE MASLOW ---
        maslow_post1 = Post.objects.create(
            author=maslow,
            caption="Diseñé esta pirámide para ilustrar cómo nuestras necesidades se organizan jerárquicamente. Desde las más básicas (fisiología y seguridad) hasta la cima de la autorrealización. ¿En qué nivel te encuentras hoy? 🔺🧠 #PsicologiaHumanista #Autorrealizacion #Maslow #Motivacion #DesarrolloPersonal #JerarquiaNecesidades",
            likes_count=8934,
            location="Brooklyn, New York"
        )
        self.assign_post_picture(maslow_post1, "maslow_post.png")

        maslow_post2 = Post.objects.create(
            author=maslow,
            caption="El crecimiento debe ser elegido una y otra vez; el miedo debe ser superado una y otra vez. La autorrealización no es un estado estático, sino un proceso continuo de desarrollo de tus potencialidades. 🌱✨ #Humanismo #CrecimientoPersonal #Motivacion #Superacion",
            likes_count=5431,
            location="University of Wisconsin-Madison"
        )
        self.assign_post_picture(maslow_post2, "maslow.png")  # Usamos su foto de perfil como segundo post

        # --- POSTS DE SKINNER ---
        skinner_post1 = Post.objects.create(
            author=skinner,
            caption="Las consecuencias de una conducta determinan la probabilidad de que vuelva a ocurrir. Mediante el refuerzo positivo fortalecemos conductas deseadas. ¿Cómo aplicas el refuerzo en tu día a día? 🐁⚡ #Conductismo #Skinner #CondicionamientoOperante #PsicologiaCientifica #Educacion #Refuerzo",
            likes_count=7421,
            location="Harvard Psychological Laboratories"
        )
        self.assign_post_picture(skinner_post1, "skinner_post.png")

        skinner_post2 = Post.objects.create(
            author=skinner,
            caption="La educación es lo que sobrevive cuando todo lo aprendido ha sido olvidado. Diseñar entornos adecuados es clave para guiar el aprendizaje y el comportamiento de manera ética y constructiva. 📚🔬 #Educacion #Behaviorismo #Aprendizaje #DisenoAmbiental",
            likes_count=4892,
            location="Cambridge, Massachusetts"
        )
        self.assign_post_picture(skinner_post2, "skinner.png")

        # --- POSTS DE MCGREGOR ---
        mcgregor_post1 = Post.objects.create(
            author=mcgregor,
            caption="El comportamiento del líder refleja sus supuestos básicos sobre la naturaleza humana. ¿Ves a tus colaboradores como perezosos que necesitan control (Teoría X) o como personas proactivas que buscan autorrealización (Teoría Y)? 👔🤝 #Liderazgo #TeoriaXTeoriaY #Administracion #MIT #RecursosHumanos #Management",
            likes_count=6120,
            location="MIT Sloan School of Management"
        )
        self.assign_post_picture(mcgregor_post1, "mcgregor_post.png")

        mcgregor_post2 = Post.objects.create(
            author=mcgregor,
            caption="El límite del crecimiento organizacional no está en la tecnología, sino en nuestra capacidad para aprovechar el potencial creativo y el compromiso de las personas bajo el liderazgo adecuado. 💡📈 #DesarrolloOrganizacional #LiderazgoY #TrabajoEnEquipo",
            likes_count=3954,
            location="Antioch College"
        )
        self.assign_post_picture(mcgregor_post2, "mcgregor.png")

        # --- POSTS DE VROOM ---
        vroom_post1 = Post.objects.create(
            author=vroom,
            caption="La motivación no es azarosa: es el resultado de un cálculo mental. Es el producto de tres variables: Expectativa (creer que tu esfuerzo rendirá frutos), Instrumentalidad (confiar en que el rendimiento traerá una recompensa) y Valencia (el valor que le das a esa recompensa). 📊🧠 #MotivacionLaboral #TeoriaExpectativas #Vroom #ComportamientoOrganizacional #Yale",
            likes_count=4321,
            location="Yale School of Management"
        )
        self.assign_post_picture(vroom_post1, "vroom_post.png")

        vroom_post2 = Post.objects.create(
            author=vroom,
            caption="El líder efectivo adapta su estilo de toma de decisiones dependiendo de la situación. Desde un enfoque netamente autocrático hasta uno completamente colaborativo, el contexto determina el éxito. 🧠🗺️ #LiderazgoSituacional #TomaDeDecisiones #Management",
            likes_count=2901,
            location="New Haven, Connecticut"
        )
        self.assign_post_picture(vroom_post2, "vroom.png")

        # --- POSTS DE HERZBERG ---
        herzberg_post1 = Post.objects.create(
            author=herzberg,
            caption="¡Cuidado! Aumentar el sueldo de un empleado evita que esté insatisfecho (Higiene), pero NO hace que esté motivado (Motivación). Para motivar de verdad, debemos enriquecer el trabajo dándole mayor autonomía, responsabilidad y crecimiento. 💼✨ #Herzberg #MotivacionHigiene #Administracion #RecursosHumanos #ClimaLaboral",
            likes_count=5871,
            location="University of Utah"
        )
        self.assign_post_picture(herzberg_post1, "herzberg_post.png")

        herzberg_post2 = Post.objects.create(
            author=herzberg,
            caption="Si quieres que alguien haga un buen trabajo, dale un buen trabajo para hacer. El enriquecimiento del puesto de trabajo es la verdadera clave para la satisfacción interna y la productividad. 💡🛠️ #EnriquecimientoLaboral #PsicologiaIndustrial #HBR #SatisfaccionLaboral",
            likes_count=4120,
            location="Pittsburgh, Pennsylvania"
        )
        self.assign_post_picture(herzberg_post2, "herzberg.png")


        self.stdout.write("Agregando comentarios cruzados (interacciones)...")

        # Comentarios en post 1 de Maslow (Jerarquía de Necesidades)
        Comment.objects.create(
            post=maslow_post1,
            author_name="bf_skinner",
            text="Interesante pirámide, Abraham. Sin embargo, considero que esas 'necesidades internas' son inaccesibles científicamente. Deberíamos centrarnos únicamente en cómo los refuerzos externos guían al individuo."
        )
        Comment.objects.create(
            post=maslow_post1,
            author_name="abraham_maslow",
            text="Entiendo tu punto de vista, Burrhus, pero reducir al ser humano a meras respuestas a estímulos externos ignora por completo nuestra búsqueda interna de significado, valores y autorrealización."
        )
        Comment.objects.create(
            post=maslow_post1,
            author_name="frederick_herzberg",
            text="Concuerdo con Abraham. En mis investigaciones de campo, el 'crecimiento' y la 'autorrealización' son los únicos motivadores verdaderos en el trabajo; las condiciones higiénicas físicas solo previenen la queja."
        )

        # Comentarios en post 1 de Skinner (Condicionamiento Operante)
        Comment.objects.create(
            post=skinner_post1,
            author_name="douglas_mcgregor",
            text="Burrhus, tu caja y el condicionamiento son brillantes. Pero si tratamos a las personas bajo controles de castigo y recompensa extrínseca en las empresas, caemos en la Teoría X. La Teoría Y busca motivadores intrínsecos."
        )
        Comment.objects.create(
            post=skinner_post1,
            author_name="bf_skinner",
            text="Douglas, la Teoría Y no es más que un diseño ambiental excelente que provee refuerzos positivos naturales y elimina los aversivos. El entorno sigue moldeando la conducta, nos guste o no."
        )

        # Comentarios en post 1 de McGregor (Teoría X y Y)
        Comment.objects.create(
            post=mcgregor_post1,
            author_name="victor_vroom",
            text="Douglas, tu clasificación X/Y es sumamente intuitiva. En mi Teoría de Expectativas, un empleado en un entorno de Teoría Y tendrá una motivación alta porque percibe que su esfuerzo sí se traducirá en recompensas valiosas."
        )
        Comment.objects.create(
            post=mcgregor_post1,
            author_name="douglas_mcgregor",
            text="Exactamente, Victor. Tu modelo le da un sustento formal y cognitivo a por qué los empleados en entornos de confianza rinden más: evalúan racionalmente su libertad de acción."
        )

        # Comentarios en post 1 de Vroom (Teoría Expectativas)
        Comment.objects.create(
            post=vroom_post1,
            author_name="frederick_herzberg",
            text="Victor, tu ecuación de motivación es impecable. Sin embargo, ten cuidado: si la 'recompensa' en tu factor de Instrumentalidad consiste solo de sueldos o condiciones físicas (Higiene), el valor de tu Valencia decaerá pronto."
        )
        Comment.objects.create(
            post=vroom_post1,
            author_name="victor_vroom",
            text="Totalmente de acuerdo, Frederick. La Valencia mide el valor subjetivo de la recompensa. Si la organización ofrece crecimiento o reconocimiento (Motivadores tuyos), la Valencia se disparará y multiplicará el esfuerzo."
        )

        # Comentarios en post 1 de Herzberg (Teoría Dos Factores)
        Comment.objects.create(
            post=herzberg_post1,
            author_name="abraham_maslow",
            text="Frederick, veo una correlación clarísima: tus factores de Higiene coinciden con mis necesidades básicas (fisiología, seguridad). Tus factores de Motivación se corresponden con la cima de mi pirámide. ¡Gran trabajo de campo!"
        )
        Comment.objects.create(
            post=herzberg_post1,
            author_name="frederick_herzberg",
            text="Gracias, Abraham. Tus marcos conceptuales sobre el potencial humano fueron, sin duda, la base e inspiración teórica para todo mi estudio empírico en la industria."
        )

        self.stdout.write(self.style.SUCCESS("Base de datos sembrada con éxito."))

    def assign_profile_picture(self, author, filename):
        src_path = os.path.join(settings.MEDIA_ROOT, "profiles", filename)
        if os.path.exists(src_path):
            with open(src_path, 'rb') as f:
                author.profile_picture.save(filename, File(f), save=True)
            self.stdout.write(f"Foto de perfil asignada a @{author.username}")
        else:
            self.stdout.write(self.style.WARNING(f"No se encontró la imagen: {src_path}"))

    def assign_post_picture(self, post, filename):
        src_path = os.path.join(settings.MEDIA_ROOT, "posts", filename)
        if os.path.exists(src_path):
            with open(src_path, 'rb') as f:
                post.image.save(filename, File(f), save=True)
            self.stdout.write(f"Imagen de post asignada al post {post.id} de @{post.author.username}")
        else:
            # Fallback en caso de usar la foto del perfil
            src_profile_path = os.path.join(settings.MEDIA_ROOT, "profiles", filename)
            if os.path.exists(src_profile_path):
                with open(src_profile_path, 'rb') as f:
                    post.image.save(filename, File(f), save=True)
                self.stdout.write(f"Imagen de post (perfil) asignada al post {post.id} de @{post.author.username}")
            else:
                self.stdout.write(self.style.WARNING(f"No se encontró la imagen de post: {src_path}"))
