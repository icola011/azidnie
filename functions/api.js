// Netlify serverless function to handle FastAPI requests
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    headers: {
      "Content-Type": "text/html",
    },
    body: `
      <!DOCTYPE html>
      <html lang="fr">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestion d'Entreprise</title>
        <link rel="stylesheet" href="/static/css/style.css">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
      </head>
      <body>
        <div class="container mt-5">
          <div class="row justify-content-center">
            <div class="col-md-8">
              <div class="card shadow">
                <div class="card-body text-center">
                  <h1 class="mb-4">Gestion d'Entreprise</h1>
                  <p class="lead">Application de gestion d'entreprise avec FastAPI et Supabase</p>
                  <div class="alert alert-info">
                    <p><strong>Note:</strong> Cette application nécessite un serveur Python pour fonctionner.</p>
                    <p>Netlify ne prend pas en charge l'exécution de serveurs Python directement.</p>
                  </div>
                  <div class="mt-4">
                    <h4>Pour exécuter cette application :</h4>
                    <ol class="text-start">
                      <li>Clonez le dépôt sur votre machine locale</li>
                      <li>Installez les dépendances avec <code>pip install -r requirements.txt</code></li>
                      <li>Configurez Supabase selon les instructions dans <code>SUPABASE_SETUP.md</code></li>
                      <li>Lancez l'application avec <code>uvicorn main:app --reload</code></li>
                    </ol>
                  </div>
                  <div class="mt-4">
                    <h4>Fonctionnalités principales :</h4>
                    <ul class="text-start">
                      <li>Gestion des factures clients et fournisseurs</li>
                      <li>Gestion de projets avec suivi de progression</li>
                      <li>Gestion des matériaux et charges</li>
                      <li>Tableau de bord avec statistiques</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
      </body>
      </html>
    `,
  };
};