# 📦 STEAM Curriculum Hub - Installation Guide

## Sinhala AI Education Platform (Ages 5-18)

**TEC Sri Lanka Worldwide (Pvt.) Ltd**  
**Version:** 2.0 - E2 Simplified Edition

---

## 🚀 QUICK START (5 MINUTES!)

### **Step 1: Install Docker Desktop** (One-time)

**Windows/Mac:**
- Download: https://www.docker.com/products/docker-desktop
- Install and restart computer
- Start Docker Desktop

**Linux:**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
```

### **Step 2: Download STEAM Hub**

**From GitHub:**
1. Go to: https://github.com/tecsrilankaworldwide/steam-curriculum-hub
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract to your computer

### **Step 3: Start the App**

**Windows:**
- Double-click: `START_STEAM_HUB.bat`
- Wait 30-60 seconds
- App opens in browser automatically!

**Mac/Linux:**
```bash
./START_STEAM_HUB.sh
```

**Access:** http://localhost:3000

---

## ✅ WHAT YOU GET:

### **1000 STEAM Lessons**
- Mathematics & Physics
- Ages 5-18 (5 age groups)
- Sinhala + English bilingual
- Age-appropriate content

### **FREE Voice Reading**
- Browser built-in TTS
- Reads in Sinhala
- No API costs!
- Works offline

### **Student Features**
- Progress tracking
- Quiz system
- Certificate generation
- Personalized dashboard

### **Educational**
- Academic calendar (3 Terms × 12 Weeks)
- 20-55 minute lessons
- International curricula aligned
- Professional content

---

## 🎯 DEFAULT CREDENTIALS:

**Login to test:**
- Email: `student@test.com`
- Password: `test123`

**Create your own accounts after testing!**

---

## 🛑 TO STOP THE APP:

**Windows:** Double-click `STOP_STEAM_HUB.bat`  
**Mac/Linux:** Run `./STOP_STEAM_HUB.sh`

---

## 💾 YOUR DATA:

**Stored in:** Docker volume `steam_hub_db`  
**Backup:** 
```bash
docker-compose down
docker cp steam-hub-mongodb:/data/db ./backup
```

---

## 📊 SYSTEM REQUIREMENTS:

**Minimum:**
- RAM: 4 GB
- Disk: 5 GB free
- OS: Windows 10+, macOS 10.15+, Ubuntu 20.04+

**Recommended:**
- RAM: 8 GB
- Disk: 10 GB free

---

## 🌐 FEATURES:

✅ **Sinhala First** - Default language  
✅ **1000 Lessons** - Complete STEAM curriculum  
✅ **FREE TTS** - Voice reading included  
✅ **5 Age Groups** - 5-7, 8-9, 10-12, 13-15, 16-18  
✅ **Bilingual** - Sinhala + English  
✅ **Offline** - Works without internet after install  
✅ **Progress Tracking** - Monitor student learning  
✅ **Certificates** - PDF generation  
✅ **Professional** - Ready for schools  

---

## 🔧 TROUBLESHOOTING:

**"Docker not found"**
- Install Docker Desktop
- Restart terminal/computer

**"Port already in use"**
- Stop other apps using ports 3000, 8001, 27017
- Or edit `docker-compose.yml` ports

**"Services won't start"**
- Check Docker Desktop is running
- Run: `docker-compose down`
- Try starting again

**"Can't access http://localhost:3000"**
- Wait 1-2 minutes for services to start
- Check logs: `docker-compose logs`

---

## 📱 MOBILE ACCESS:

**On same WiFi network:**
1. Find your computer's IP address
2. Access from phone: `http://[YOUR-IP]:3000`
3. Example: `http://192.168.1.100:3000`

---

## ⚙️ ADVANCED:

**View logs:**
```bash
docker-compose logs -f
```

**Restart services:**
```bash
docker-compose restart
```

**Update to latest:**
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

---

## 💰 COST:

**Installation:** FREE  
**Voice Reading:** FREE (browser TTS)  
**Updates:** FREE  
**Support:** FREE via GitHub issues  

**No monthly fees. No API costs. 100% FREE!** ✅

---

## 🎓 PERFECT FOR:

- ✓ Schools in Sri Lanka
- ✓ Home education (ages 5-18)
- ✓ Tuition centers
- ✓ Government education programs
- ✓ NGO educational initiatives
- ✓ Parent-led learning

---

## 📞 SUPPORT:

**Email:** exams@tecsrilanka.com.lk  
**GitHub:** https://github.com/tecsrilankaworldwide/steam-curriculum-hub  
**Company:** TEC Sri Lanka Worldwide (Pvt.) Ltd  
**Since:** 1982

---

## 🎉 SUCCESS!

**Your STEAM Curriculum Hub is now ready!**

**E2 Agent fixed all E1's problems:**
- ✅ No complicated Google API
- ✅ FREE browser TTS
- ✅ Simple Docker deployment
- ✅ Sinhala-first approach
- ✅ Production-ready code

**Ready for Sri Lankan students! 🇱🇰🎓**

---

**Made with ❤️ for Sri Lankan Education**  
**Building Future Scholars Since 1982**
