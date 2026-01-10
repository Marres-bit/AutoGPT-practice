# ☁️ Configuration Cloud pour MediGenius AI

## Mode Gratuit (Par défaut)

MediGenius AI fonctionne **immédiatement en mode gratuit** avec JSONBin.io !

Aucune configuration requise - le système créera automatiquement un bin cloud lors du premier enregistrement.

## Mode Premium (Optionnel)

Pour plus de capacité de stockage :

### 1. Créer un compte JSONBin.io

1. Allez sur https://jsonbin.io
2. Créez un compte gratuit
3. Copiez votre clé API

### 2. Configurer la clé

Ajoutez dans votre fichier `.env` :

```env
OPENAI_API_KEY=votre_cle_openai
JSONBIN_API_KEY=votre_cle_jsonbin
```

### 3. Redémarrer l'application

```bash
python main_medical.py
```

## Migration depuis SQLite

Si vous aviez des leçons dans la base locale :

```bash
python migrate_to_cloud.py
```

Ceci migrera toutes vos leçons vers le cloud.

## Avantages du Cloud

✅ **Accessible partout** - Vos leçons sur tous vos appareils
✅ **Sauvegarde automatique** - Pas de risque de perte
✅ **Synchronisation** - Toujours à jour
✅ **Cache local** - Fonctionne hors-ligne
✅ **Gratuit** - Mode gratuit inclus

## Fonctionnement

### Synchronisation Automatique

- **Ajout de leçon** → Sync immédiate vers cloud
- **Génération auto** → Sync après chaque leçon
- **Démarrage** → Télécharge les données cloud

### Cache Local

Un cache local (`cloud_cache.json`) est maintenu pour :
- Fonctionnement hors-ligne
- Rapidité d'accès
- Résilience

### Gestion des Conflits

En cas de conflit, le cloud a priorité.

## Commandes

### Voir les statistiques cloud

```bash
python main_medical.py --stats
```

### Exporter toutes les leçons

Dans l'interface :
```
/export
```

### Forcer la synchronisation

```bash
python -c "from medical_agent.cloud_database import CloudDatabase; db = CloudDatabase(); db.sync_from_cloud()"
```

## Dépannage

### Erreur de connexion

```
❌ Erreur connexion cloud
```

**Solution** : Vérifiez votre connexion Internet. Le système utilisera le cache local en attendant.

### Bin non trouvé

```
⚠️ Aucun bin configuré
```

**Solution** : Ajoutez une leçon - un nouveau bin sera créé automatiquement.

### Mode hors-ligne

Si pas de connexion Internet :
- Les leçons sont lues depuis le cache local
- Les nouvelles leçons sont sauvegardées localement
- Sync automatique au retour de la connexion

## Support

Pour toute question :
1. Vérifiez votre clé API OpenAI dans `.env`
2. Testez la connexion cloud
3. Consultez `cloud_cache.json` pour voir les données locales

---

**🧠 MediGenius AI - Intelligence médicale dans le cloud !**
