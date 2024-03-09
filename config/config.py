import os
import datetime
import json

SECRET_KEY = 'development'

class Config:
    #####################################################
    # ARCHITECTURE CONFIGURATION
    SECRET_KEY      = 'NationalSecurityUltimateSecretPassword'
    REDIS_URL       = "redis://redisserver:6379"
    CELERY_CONFIG   = {
        'broker_url'     : 'redis://localhost:6379',
        'result_backend' : 'redis://localhost:6379',
    }


    #####################################################
    # APP CONFIGURATION
    SITES               = ["https://receive-smss.com"]
    EXCLUDED_DOMAINS    = ['mrspin.co.uk']

    METADATA_INTERESTING_YES = "YES"
    METADATA_INTERESTING_NO = "NO"
    METADATA_INTERESTING_UNKNOWN = "UNKNOWN"
    
    LIST_METADATA_INTERESTING = [
        "YES",
        "NO",
        "UNKNOWN"
    ]
    
    LIST_METADATA_INTERESTING_YES = [
        "DATA_INTERESTING_DESC_YES_PII",
        "DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER",
        "DATA_INTERESTING_DESC_YES_DISCOVERY",
        "DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET"
    ]

    LIST_METADATA_INTERESTING_NO = [
        "DATA_INTERESTING_DESC_NO_SCAM",
        "DATA_INTERESTING_DESC_NO_AD",
        "DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY",
        "DATA_INTERESTING_DESC_NO_OTHER"
    ]

    METADATA = {
        "data" : [
            {
                "domain":"ig.me",
                "is_automated":False,
                "is_interesting":True,
                "is_interesting_desc":[
                    "DATA_INTERESTING_DESC_YES_PII",
                    "DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER"
                ]
            },
            {
                "domain":"nps.airindia.in",
                "is_automated":True,
                "is_interesting":True,
                "is_interesting_desc":[
                    "DATA_INTERESTING_DESC_YES_PII",
                    "DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER"
                ]
            },
            {
                "domain":"mrspin.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":[
                    "DATA_INTERESTING_DESC_NO_SCAM"
                ]
            },
            {
                "domain":"superprof.es",
                "is_automated":True,
                "is_interesting":True,
                "is_interesting_desc":[
                    "DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER"
                ]
            },
            {
                "domain":"cns-sante-lu.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"aba2.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"fashionnovagb.attn.tv",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"traba.page.link",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"financiar24.es",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"www.snagshout.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"vent.africa",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"auth.usbank.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"pp24.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"bnc.lt",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"idmcn-web.deployer.mx",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"gallery-victoria.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"t.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"4go.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"mdslt.win",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"sports.bet9ja.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"amznsa.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"bbva.netcash-clientes-es.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"wnc.es",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"dhljjs.top",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"txts.ly",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"eskimo.page.link",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"clk.mk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"turbotax.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"wilkinsonswordintuition.zptr.im",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"tmbo.la",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"boom.lat",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"9mc.onelink.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"square-register.onelink.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"url.ez4u.pt",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.freestuff.eu",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"nxt.to",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"ejmj.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"versalie.sandbox01.wheel.health",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"amazon.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"u.to",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"accuweb.cloud",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"bbva.es-notificacionapp.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"wmecs.net",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"apple.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"pcpe1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"fscr.io",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"gamblii.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"vimeo.com",
                "is_automated":False,
                "is_interesting":True,
                "is_interesting_desc":["DATA_INTERESTING_DESC_YES_PII"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"18u.one",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"veriff.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"app.konto.com",
                "is_automated":False,
                "is_interesting":True,
                "is_interesting_desc":["DATA_INTERESTING_DESC_YES_PII"]
            },
            {
                "domain":"cash.app",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"i.nos.pt",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"ae.goldenscent.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.bidfta.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"103.13.209.127",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"usfi1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"brz.ai",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"mobile.three.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"app.temu.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"device.staging.payfone.com:4443",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"a.klar.na",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"wh.bet",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"dhljle.top",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"suitsmecard.com",
                "is_automated":False,
                "is_interesting":True,
                "is_interesting_desc":["DATA_INTERESTING_DESC_YES_PII"]
            },
            {
                "domain":"bnk.la",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"t.xfin.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"txt.rwdsuk.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"my.photoday.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"id.ubble.ai",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"gtln2.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"chime.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"walgreens.sandbox01.wheel.health",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"www.crhlth.to",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"betsson.fr",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"m.gopuff.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"www.zigota.co.il",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"support.strip",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"gxmble.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"www.yychomes.net",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"zappit.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"mrspin.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"kvy8.io",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"help.super.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"amazon.pl",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"blu1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"gcpayonline.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"airdrop-bybit.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"smsq.com.de",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"eej.at",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"dd.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"prm.ms",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"l.mrbit.vin",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"ewzvve.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"jb4.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"app.inkind.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"lock.authvia.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":[""]
            },
            {
                "domain":"lyft.sng.link",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"gra.cx",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"tiny.one",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"oot.rs",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"trn1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"support.bondora.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"py.pl",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"kcs-airdrop.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"gl0.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"fntl1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"inboxd.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"www.amazon.it",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"sd2.in",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"yelp.to",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"signal.org",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"updatesafetymyid.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"seven.casino",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"unv.viber.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"tinyurl.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"hadotx.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"device.proveapis.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"bbva.inicio-es.info",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"homa1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"dinr.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"82link.cc",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"ehplabsuk.smsb.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"es.bbva-soporte-clientes.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"kikoff.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"pplchck.com",
                "is_automated":False,
                "is_interesting":True,
                "is_interesting_desc":["DATA_INTERESTING_DESC_YES_PII"]
            },
            {
                "domain":"intch1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"craftd.pscrpt.io",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"ijcpct.in",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"revolut.onelink.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"wilkinsonsword.zptr.im",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"a.lott.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"verfy.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":[""]
            },
            {
                "domain":"news.sfcollege.edu",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"apply.oportun.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"mobile.bet9ja.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"nvosms.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"biy.io",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"nos.pt",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"]
            },
            {
                "domain":"www.o2.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.shaadi.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"ptxt.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"stk9998.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"moj.doublestar.sk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"teya.cc",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"app.adjust.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"google.net",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"nbet.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"pimedigital.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"pscrpt.io",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"launchapp.credas.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"lensa.ro",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"keny.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"hqy.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"app.cm.ourcart.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"recovery.careem.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"ola351.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"bap.mx",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"my4.uno",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":[""]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":True,
                "is_interesting_desc":["DATA_INTERESTING_DESC_YES_PII"]
            },
            {
                "domain":"dhlsfdd.top",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"hoi.fm",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":[""]
            },
            {
                "domain":"vivavida.onelink.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.checkatrade.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"fdea.io",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"aka.ms",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"optxt.net",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"t.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"ukrwdz.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"acs1.tc",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"mn1.uno",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"emujac.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"phongvantech.vn",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"trb1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"amazon.de",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"WNDRSKN.smsb.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"amazon.es",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"t.uber.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"ospt.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"ebmm1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"super.sng.link",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"facebook-update0.blog",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"reports.viber.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"yahoo.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"shorturl.at",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"#VALEUR!",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"store.playwing.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"byt.tips",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"ccs1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"amazon.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"tx.vc",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"gt.sms247.de",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"itbl.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"mfort.win",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"cl17.xyz",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"www.vandalay.in",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"contrato.totalenergies.es",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"wuqsl.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"abre.ai",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"fjn.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":[""]
            },
            {
                "domain":"ruadapalma.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"new.three.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"current.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"bit.ly",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"yxeeh.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"links.hearclear.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"c.rocket.la",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD"]
            },
            {
                "domain":"joli88.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"google.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"dexatel.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"lcuk.win",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"txte1.co",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_AD","DATA_INTERESTING_DESC_NO_SCAM"]
            },
            {
                "domain":"is.gd",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"lng.direct-inicio-apps.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"wa.me",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.zopa.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"foliatticasino.mx",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"ridleyacad.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.authy.com",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"www.vodafone.co.uk",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            },
            {
                "domain":"cred.ee",
                "is_automated":False,
                "is_interesting":False,
                "is_interesting_desc":["DATA_INTERESTING_DESC_NO_OTHER"]
            }
        ]
    }

    def getApplicationStatus():
        #####################################################
        # APP CONFIGURATION - SERACH FILTERS
        DATA_AUTOMATED_YES                                  = []
        DATA_AUTOMATED_NO                                   = []
        DATA_INTERESTING_YES                                = []
        DATA_INTERESTING_NO                                 = []
        DATA_INTERESTING_DESC_NO_SCAM                       = []
        DATA_INTERESTING_DESC_NO_AD                         = []
        DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY         = []
        DATA_INTERESTING_DESC_NO_OTHER                      = []
        DATA_INTERESTING_DESC_YES_PII                       = []
        DATA_INTERESTING_DESC_YES_DISCOVERY                 = []
        DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER          = []
        DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET    = []

        for item in Config.METADATA['data']:

            # AUTOMATED
            if item['is_automated'] == True:
                DATA_AUTOMATED_YES.append(item['domain'])
            else: 
                DATA_AUTOMATED_NO.append(item['domain'])

            # INTERESING
            if item['is_interesting'] == True:
                DATA_INTERESTING_YES.append(item['domain'])
            else: 
                DATA_INTERESTING_NO.append(item['domain'])

            # NO INTERESING DESC 
            if "DATA_INTERESTING_DESC_NO_SCAM"                 in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_NO_SCAM.append(item['domain'])
            if "DATA_INTERESTING_DESC_NO_AD"                   in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_NO_AD.append(item['domain'])
            if "DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"   in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY.append(item['domain'])
            if "DATA_INTERESTING_DESC_NO_OTHER"                in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_NO_OTHER.append(item['domain'])
            if "DATA_INTERESTING_DESC_NO_OTHER"                in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_NO_OTHER.append(item['domain'])

            # INTERESING DESC 
            if "DATA_INTERESTING_DESC_YES_PII"                                      in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_YES_PII.append(item['domain'])
            if "DATA_INTERESTING_DESC_YES_DISCOVERY"                                in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_YES_DISCOVERY.append(item['domain'])
            if "DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER"                         in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER.append(item['domain'])
            if "DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET"                   in item['is_interesting_desc']:
                DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET.append(item['domain'])

        TARGET_DATA = {}
        TARGET_DATA['DATA_AUTOMATED_YES']                               = DATA_AUTOMATED_YES
        TARGET_DATA['DATA_AUTOMATED_NO']                                = DATA_AUTOMATED_NO
        TARGET_DATA['DATA_INTERESTING_YES']                             = DATA_INTERESTING_YES
        TARGET_DATA['DATA_INTERESTING_NO']                              = DATA_INTERESTING_NO
        TARGET_DATA['DATA_INTERESTING_DESC_NO_SCAM']                    = DATA_INTERESTING_DESC_NO_SCAM
        TARGET_DATA['DATA_INTERESTING_DESC_NO_AD']                      = DATA_INTERESTING_DESC_NO_AD
        TARGET_DATA['DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY']      = DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY
        TARGET_DATA['DATA_INTERESTING_DESC_NO_OTHER']                   = DATA_INTERESTING_DESC_NO_OTHER
        TARGET_DATA['DATA_INTERESTING_DESC_YES_PII']                    = DATA_INTERESTING_DESC_YES_PII
        TARGET_DATA['DATA_INTERESTING_DESC_YES_DISCOVERY']              = DATA_INTERESTING_DESC_YES_DISCOVERY
        TARGET_DATA['DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER']       = DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER
        TARGET_DATA['DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET'] = DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET
        
        return TARGET_DATA

    SEARCH_URL = [
        'nps.airindia.in'
    ]

    SEARCH_FILTERS_DATA = [
        'NONE',
        'YES',
        'NO'
    ]

    SEARCH_FILTERS_INTERESTING = [
        'NONE',
        'YES',
        'NO',
        'ALL'
    ]



class Connections:
    DATABASE = 'postgres'
    USER = 'postgres'
    PASSWORD = 'FileExposer'
    HOST = 'database'
    PORT='5432'

class Phone:
    COUNTRIES = [
        {"code": "+7 840","name": "Abkhazia"},
        {"code": "+93","name": "Afghanistan"},
        {"code": "+355","name": "Albania"},
        {"code": "+213","name": "Algeria"},
        {"code": "+1 684","name": "American Samoa"},
        {"code": "+376","name": "Andorra"},
        {"code": "+244","name": "Angola"},
        {"code": "+1 264","name": "Anguilla"},
        {"code": "+1 268","name": "Antigua and Barbuda"},
        {"code": "+54","name": "Argentina"},
        {"code": "+374","name": "Armenia"},
        {"code": "+297","name": "Aruba"},
        {"code": "+247","name": "Ascension"},
        {"code": "+61","name": "Australia"},
        {"code": "+672","name": "Australian External Territories"},
        {"code": "+43","name": "Austria"},
        {"code": "+994","name": "Azerbaijan"},
        {"code": "+1 242","name": "Bahamas"},
        {"code": "+973","name": "Bahrain"},
        {"code": "+880","name": "Bangladesh"},
        {"code": "+1 246","name": "Barbados"},
        {"code": "+1 268","name": "Barbuda"},
        {"code": "+375","name": "Belarus"},
        {"code": "+32","name": "Belgium"},
        {"code": "+501","name": "Belize"},
        {"code": "+229","name": "Benin"},
        {"code": "+1 441","name": "Bermuda"},
        {"code": "+975","name": "Bhutan"},
        {"code": "+591","name": "Bolivia"},
        {"code": "+387","name": "Bosnia and Herzegovina"},
        {"code": "+267","name": "Botswana"},
        {"code": "+55","name": "Brazil"},
        {"code": "+246","name": "British Indian Ocean Territory"},
        {"code": "+1 284","name": "British Virgin Islands"},
        {"code": "+673","name": "Brunei"},
        {"code": "+359","name": "Bulgaria"},
        {"code": "+226","name": "Burkina Faso"},
        {"code": "+257","name": "Burundi"},
        {"code": "+855","name": "Cambodia"},
        {"code": "+237","name": "Cameroon"},
        {"code": "+1","name": "Canada"},
        {"code": "+238","name": "Cape Verde"},
        {"code": "+ 345","name": "Cayman Islands"},
        {"code": "+236","name": "Central African Republic"},
        {"code": "+235","name": "Chad"},
        {"code": "+56","name": "Chile"},
        {"code": "+86","name": "China"},
        {"code": "+61","name": "Christmas Island"},
        {"code": "+61","name": "Cocos-Keeling Islands"},
        {"code": "+57","name": "Colombia"},
        {"code": "+269","name": "Comoros"},
        {"code": "+242","name": "Congo"},
        {"code": "+243","name": "Congo, Dem. Rep. of (Zaire)"},
        {"code": "+682","name": "Cook Islands"},
        {"code": "+506","name": "Costa Rica"},
        {"code": "+385","name": "Croatia"},
        {"code": "+53","name": "Cuba"},
        {"code": "+599","name": "Curacao"},
        {"code": "+537","name": "Cyprus"},
        {"code": "+420","name": "Czech Republic"},
        {"code": "+45","name": "Denmark"},
        {"code": "+246","name": "Diego Garcia"},
        {"code": "+253","name": "Djibouti"},
        {"code": "+1 767","name": "Dominica"},
        {"code": "+1 809","name": "Dominican Republic"},
        {"code": "+670","name": "East Timor"},
        {"code": "+56","name": "Easter Island"},
        {"code": "+593","name": "Ecuador"},
        {"code": "+20","name": "Egypt"},
        {"code": "+503","name": "El Salvador"},
        {"code": "+240","name": "Equatorial Guinea"},
        {"code": "+291","name": "Eritrea"},
        {"code": "+372","name": "Estonia"},
        {"code": "+251","name": "Ethiopia"},
        {"code": "+500","name": "Falkland Islands"},
        {"code": "+298","name": "Faroe Islands"},
        {"code": "+679","name": "Fiji"},
        {"code": "+358","name": "Finland"},
        {"code": "+33","name": "France"},
        {"code": "+596","name": "French Antilles"},
        {"code": "+594","name": "French Guiana"},
        {"code": "+689","name": "French Polynesia"},
        {"code": "+241","name": "Gabon"},
        {"code": "+220","name": "Gambia"},
        {"code": "+995","name": "Georgia"},
        {"code": "+49","name": "Germany"},
        {"code": "+233","name": "Ghana"},
        {"code": "+350","name": "Gibraltar"},
        {"code": "+30","name": "Greece"},
        {"code": "+299","name": "Greenland"},
        {"code": "+1 473","name": "Grenada"},
        {"code": "+590","name": "Guadeloupe"},
        {"code": "+1 67","name": "Guam"},
        {"code": "+502","name": "Guatemala"},
        {"code": "+224","name": "Guinea"},
        {"code": "+245","name": "Guinea-Bissau"},
        {"code": "+595","name": "Guyana"},
        {"code": "+509","name": "Haiti"},
        {"code": "+504","name": "Honduras"},
        {"code": "+852","name": "Hong Kong SAR China"},
        {"code": "+36","name": "Hungary"},
        {"code": "+354","name": "Iceland"},
        {"code": "+91","name": "India"},
        {"code": "+62","name": "Indonesia"},
        {"code": "+98","name": "Iran"},
        {"code": "+964","name": "Iraq"},
        {"code": "+353","name": "Ireland"},
        {"code": "+972","name": "Israel"},
        {"code": "+39","name": "Italy"},
        {"code": "+225","name": "Ivory Coast"},
        {"code": "+1 876","name": "Jamaica"},
        {"code": "+81","name": "Japan"},
        {"code": "+962","name": "Jordan"},
        {"code": "+7 7","name": "Kazakhstan"},
        {"code": "+254","name": "Kenya"},
        {"code": "+686","name": "Kiribati"},
        {"code": "+965","name": "Kuwait"},
        {"code": "+996","name": "Kyrgyzstan"},
        {"code": "+856","name": "Laos"},
        {"code": "+371","name": "Latvia"},
        {"code": "+961","name": "Lebanon"},
        {"code": "+266","name": "Lesotho"},
        {"code": "+231","name": "Liberia"},
        {"code": "+218","name": "Libya"},
        {"code": "+423","name": "Liechtenstein"},
        {"code": "+370","name": "Lithuania"},
        {"code": "+352","name": "Luxembourg"},
        {"code": "+853","name": "Macau SAR China"},
        {"code": "+389","name": "Macedonia"},
        {"code": "+261","name": "Madagascar"},
        {"code": "+265","name": "Malawi"},
        {"code": "+60","name": "Malaysia"},
        {"code": "+960","name": "Maldives"},
        {"code": "+223","name": "Mali"},
        {"code": "+356","name": "Malta"},
        {"code": "+692","name": "Marshall Islands"},
        {"code": "+596","name": "Martinique"},
        {"code": "+222","name": "Mauritania"},
        {"code": "+230","name": "Mauritius"},
        {"code": "+262","name": "Mayotte"},
        {"code": "+52","name": "Mexico"},
        {"code": "+691","name": "Micronesia"},
        {"code": "+1 808","name": "Midway Island"},
        {"code": "+373","name": "Moldova"},
        {"code": "+377","name": "Monaco"},
        {"code": "+976","name": "Mongolia"},
        {"code": "+382","name": "Montenegro"},
        {"code": "+1664","name": "Montserrat"},
        {"code": "+212","name": "Morocco"},
        {"code": "+95","name": "Myanmar"},
        {"code": "+264","name": "Namibia"},
        {"code": "+674","name": "Nauru"},
        {"code": "+977","name": "Nepal"},
        {"code": "+31","name": "Netherlands"},
        {"code": "+599","name": "Netherlands Antilles"},
        {"code": "+1 869","name": "Nevis"},
        {"code": "+687","name": "New Caledonia"},
        {"code": "+64","name": "New Zealand"},
        {"code": "+505","name": "Nicaragua"},
        {"code": "+227","name": "Niger"},
        {"code": "+234","name": "Nigeria"},
        {"code": "+683","name": "Niue"},
        {"code": "+672","name": "Norfolk Island"},
        {"code": "+850","name": "North Korea"},
        {"code": "+1 670","name": "Northern Mariana Islands"},
        {"code": "+47","name": "Norway"},
        {"code": "+968","name": "Oman"},
        {"code": "+92","name": "Pakistan"},
        {"code": "+680","name": "Palau"},
        {"code": "+970","name": "Palestinian Territory"},
        {"code": "+507","name": "Panama"},
        {"code": "+675","name": "Papua New Guinea"},
        {"code": "+595","name": "Paraguay"},
        {"code": "+51","name": "Peru"},
        {"code": "+63","name": "Philippines"},
        {"code": "+48","name": "Poland"},
        {"code": "+351","name": "Portugal"},
        {"code": "+1 787","name": "Puerto Rico"},
        {"code": "+974","name": "Qatar"},
        {"code": "+262","name": "Reunion"},
        {"code": "+40","name": "Romania"},
        {"code": "+7","name": "Russia"},
        {"code": "+250","name": "Rwanda"},
        {"code": "+685","name": "Samoa"},
        {"code": "+378","name": "San Marino"},
        {"code": "+966","name": "Saudi Arabia"},
        {"code": "+221","name": "Senegal"},
        {"code": "+381","name": "Serbia"},
        {"code": "+248","name": "Seychelles"},
        {"code": "+232","name": "Sierra Leone"},
        {"code": "+65","name": "Singapore"},
        {"code": "+421","name": "Slovakia"},
        {"code": "+386","name": "Slovenia"},
        {"code": "+677","name": "Solomon Islands"},
        {"code": "+27","name": "South Africa"},
        {"code": "+500","name": "South Georgia and the South Sandwich Islands"},
        {"code": "+82","name": "South Korea"},
        {"code": "+34","name": "Spain"},
        {"code": "+94","name": "Sri Lanka"},
        {"code": "+249","name": "Sudan"},
        {"code": "+597","name": "Suriname"},
        {"code": "+268","name": "Swaziland"},
        {"code": "+46","name": "Sweden"},
        {"code": "+41","name": "Switzerland"},
        {"code": "+963","name": "Syria"},
        {"code": "+886","name": "Taiwan"},
        {"code": "+992","name": "Tajikistan"},
        {"code": "+255","name": "Tanzania"},
        {"code": "+66","name": "Thailand"},
        {"code": "+670","name": "Timor Leste"},
        {"code": "+228","name": "Togo"},
        {"code": "+690","name": "Tokelau"},
        {"code": "+676","name": "Tonga"},
        {"code": "+1 868","name": "Trinidad and Tobago"},
        {"code": "+216","name": "Tunisia"},
        {"code": "+90","name": "Turkey"},
        {"code": "+993","name": "Turkmenistan"},
        {"code": "+1 649","name": "Turks and Caicos Islands"},
        {"code": "+688","name": "Tuvalu"},
        {"code": "+1 340","name": "U.S. Virgin Islands"},
        {"code": "+256","name": "Uganda"},
        {"code": "+380","name": "Ukraine"},
        {"code": "+971","name": "United Arab Emirates"},
        {"code": "+44","name": "United Kingdom"},
        {"code": "+1","name": "United States"},
        {"code": "+598","name": "Uruguay"},
        {"code": "+998","name": "Uzbekistan"},
        {"code": "+678","name": "Vanuatu"},
        {"code": "+58","name": "Venezuela"},
        {"code": "+84","name": "Vietnam"},
        {"code": "+1 808","name": "Wake Island"},
        {"code": "+681","name": "Wallis and Futuna"},
        {"code": "+967","name": "Yemen"},
        {"code": "+260","name": "Zambia"},
        {"code": "+255","name": "Zanzibar"},
        {"code": "+263","name": "Zimbabwe"}
    ]

class Logger:
    def get_date():
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S"))

    def err(s):
        with open("err.log", "a") as f:
            f.write(Logger.get_date() + '\t' + s + '\n')

    def log(s):
        with open("logfile.log", "a") as f:
            f.write(Logger.get_date() + '\t' + s + '\n')