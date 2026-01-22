"""
Test de la NOUVELLE stratégie : TOP modèles HOT et populaires
"""
from pathlib import Path
from datetime import datetime
from insanity_scanner import GEISConfig
from insanity_scanner.report_generator import ReportGenerator

def create_hot_models_demo():
    """Crée des documents Word de test pour TOP modèles HOT"""
    
    print("="*70)
    print("🔥 NOUVELLE STRATÉGIE : TOP MODÈLES HOT & POPULAIRES")
    print("="*70)
    print()
    
    config = GEISConfig()
    report_gen = ReportGenerator(config)
    
    print("⚙️ NOUVELLE CONFIGURATION:")
    print(f"   ✅ Min vues: {config.instagram_min_views:,}")
    print(f"   ✅ Min likes: {config.instagram_min_likes:,}")
    print(f"   ✅ Min followers: {config.instagram_min_followers:,}")
    print()
    
    # Données de test (TOP modèles fictifs)
    hot_models = [
        {
            'id': 'instagram_hot001',
            'source': 'instagram',
            'type': 'video_post',
            'username': 'hotmodel_sophia',
            'post_url': 'https://www.instagram.com/p/HotPost001/',
            'profile_url': 'https://www.instagram.com/hotmodel_sophia/',
            'video_views': 287543,  # 287k vues !
            'followers': 850000,     # 850k followers !
            'likes': 15234,          # 15k likes !
            'comments': 892,
            'engagement_rate': 1.89,
            'popularity_score': 125678,
            'caption': '🔥 New exclusive content dropping today! Link in bio for VIP access 💋 #model #hot',
            'onlyfans_link': 'https://onlyfans.com/hotmodel_sophia',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 'instagram_hot002',
            'source': 'instagram',
            'type': 'video_post',
            'username': 'goddess_mia',
            'post_url': 'https://www.instagram.com/p/HotPost002/',
            'profile_url': 'https://www.instagram.com/goddess_mia/',
            'video_views': 542891,  # 542k vues !!
            'followers': 1200000,    # 1.2M followers !!
            'likes': 28456,          # 28k likes !!
            'comments': 1543,
            'engagement_rate': 2.50,
            'popularity_score': 198543,
            'caption': '💎 Behind the scenes... Join my VIP page for the full experience 😘',
            'onlyfans_link': 'https://onlyfans.com/goddess_mia',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 'instagram_hot003',
            'source': 'instagram',
            'type': 'video_post',
            'username': 'queen_isabella',
            'post_url': 'https://www.instagram.com/p/HotPost003/',
            'profile_url': 'https://www.instagram.com/queen_isabella/',
            'video_views': 198765,  # 198k vues
            'followers': 650000,     # 650k followers
            'likes': 12890,          # 12k likes
            'comments': 678,
            'engagement_rate': 2.08,
            'popularity_score': 98432,
            'caption': '✨ Special surprise for my OnlyFans subscribers tonight! 🌙',
            'onlyfans_link': 'https://onlyfans.com/queen_isabella',
            'created_at': datetime.now().isoformat()
        }
    ]
    
    print(f"📁 Dossier de sortie: {config.onlyfans_output_dir}")
    print()
    print("🔥 Génération des TOP modèles HOT...")
    print()
    
    generated_docs = []
    
    for idx, model in enumerate(hot_models, 1):
        try:
            print(f"🔥 Modèle {idx}/3: @{model['username']}")
            print(f"   📊 {model['video_views']:,} vues | {model['likes']:,} likes | {model['followers']:,} followers")
            print(f"   💎 Score popularité: {model['popularity_score']:,}")
            
            doc_path = report_gen.generate(model, insanity_number=0)
            generated_docs.append(doc_path)
            print(f"   ✅ Document créé: {doc_path.name}")
            print()
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    print("="*70)
    print("✅ GÉNÉRATION TERMINÉE")
    print("="*70)
    print(f"📊 Total: {len(generated_docs)} documents Word créés")
    print()
    
    if generated_docs:
        print("📂 TOP Modèles générés:")
        for doc in generated_docs:
            print(f"   🔥 {doc.parent.name}\\{doc.name}")
        
        print()
        print("💡 Différences avec l'ancienne version:")
        print("   ❌ AVANT: Vidéos avec max 200 vues (petits comptes)")
        print("   ✅ MAINTENANT: Vidéos avec MIN 10k vues (TOP modèles)")
        print()
        print("   ❌ AVANT: Faible engagement")
        print("   ✅ MAINTENANT: Engagement massif (likes, commentaires)")
        print()
        print("   ❌ AVANT: Potentiel de croissance")
        print("   ✅ MAINTENANT: Modèles VIRALES déjà établies")
        print()
        print("🔥 Les liens Instagram et OnlyFans sont CLIQUABLES dans Word")
    
    # Afficher statistiques
    print()
    print("="*70)
    print("📊 STATISTIQUES DES TOP MODÈLES")
    print("="*70)
    
    total_views = sum(m['video_views'] for m in hot_models)
    total_likes = sum(m['likes'] for m in hot_models)
    avg_engagement = sum(m['engagement_rate'] for m in hot_models) / len(hot_models)
    
    print(f"📈 Vues totales: {total_views:,}")
    print(f"❤️ Likes totaux: {total_likes:,}")
    print(f"📊 Engagement moyen: {avg_engagement:.2f}%")
    print()
    print("🔥 Ce sont les VRAIES stars d'Instagram/OnlyFans!")

if __name__ == "__main__":
    create_hot_models_demo()
