import requests
import bs4
from telebot import TeleBot
from threading import Thread
import os
from uuid import uuid4
import xlsxwriter
import time


class Parser999md:
    def __init__(self, bot: TeleBot) -> None:
        self.bot: TeleBot = bot

    categories = [
        {"title": "Недвижемость", "id": "999_nedviga", "links": [
            'https://m.999.md/ru/list/real-estate/apartments-and-rooms',
            'https://m.999.md/ru/list/real-estate/house-and-garden',
            'https://m.999.md/ru/list/real-estate/land',
            'https://m.999.md/ru/list/real-estate/commercial-real-estate',
            'https://m.999.md/ru/list/real-estate/real-estate-abroad'
        ]},
        {
            "title": "Техника", "id": "999_tech", "links": [
                'https://m.999.md/ru/list/phone-and-communication/mobile-phones',
                'https://m.999.md/ru/list/phone-and-communication/charger-and-batteries',
                'https://m.999.md/ru/list/phone-and-communication/miscellaneous',
                'https://m.999.md/ru/list/phone-and-communication/gadget',
                'https://m.999.md/ru/list/phone-and-communication/service-and-repair-of-telephones',
            ]
        },
        {
            "title": "Авто", "id": "999_cars", "links": ['https://m.999.md/ru/list/transport/cars', 'https://m.999.md/ru/list/transport/buses-and-minibuses', 'https://m.999.md/ru/list/transport/trucks', 'https://m.999.md/ru/list/transport/motorcycles', 'https://m.999.md/ru/list/transport/bicycles', 'https://m.999.md/ru/list/transport/electric-scooters', 'https://m.999.md/ru/list/agriculture/agricultural-machinery', 'https://m.999.md/ru/list/transport/special-equipment', 'https://m.999.md/ru/list/transport/trailers', 'https://m.999.md/ru/list/construction-and-repair/construction-equipment', 'https://m.999.md/ru/list/transport/retro-cars', 'https://m.999.md/ru/list/transport/snowmobiles-and-jet-ski', 'https://m.999.md/ru/list/transport/airplanes', 'https://m.999.md/ru/list/transport/wheels-and-tires', 'https://m.999.md/ru/list/transport/spare-parts-for-cars', 'https://m.999.md/ru/list/transport/moto-equipment', 'https://m.999.md/ru/list/transport/spare-parts-for-trucks', 'https://m.999.md/ru/list/transport/auto-glass-and-optics', 'https://m.999.md/ru/list/transport/spare-parts-for-motorcycles', 'https://m.999.md/ru/list/transport/spare-parts-for-bicycles', 'https://m.999.md/ru/list/transport/batteries', 'https://m.999.md/ru/list/transport/carcaraudio', 'https://m.999.md/ru/list/transport/acoustic', 'https://m.999.md/ru/list/transport/video-recorders', 'https://m.999.md/ru/list/transport/dvd-tv-gps-tuner', 'https://m.999.md/ru/list/transport/supplies-of-car-audio', 'https://m.999.md/ru/list/transport/radars-alarms', 'https://m.999.md/ru/list/transport/interior-accessories', 'https://m.999.md/ru/list/transport/car-carpets', 'https://m.999.md/ru/list/transport/car-paint', 'https://m.999.md/ru/list/transport/technical-support', 'https://m.999.md/ru/list/transport/car-body-accessories', 'https://m.999.md/ru/list/children-world/car', 'https://m.999.md/ru/list/transport/car-trunks', 'https://m.999.md/ru/list/transport/wheel-arch-liners', 'https://m.999.md/ru/list/transport/parktronic', 'https://m.999.md/ru/list/transport/car-keys', 'https://m.999.md/ru/list/transport/keys', 'https://m.999.md/ru/list/transport/car-jacks', 'https://m.999.md/ru/list/transport/car-lifts', 'https://m.999.md/ru/list/transport/pullers', 'https://m.999.md/ru/list/transport/automobile-compressors', 'https://m.999.md/ru/list/transport/wheel-alignment-stand', 'https://m.999.md/ru/list/transport/chargers-for-cars', 'https://m.999.md/ru/list/transport/pressure-washers', 'https://m.999.md/ru/list/transport/diagnostic-equipment', 'https://m.999.md/ru/list/transport/tire-equipment', 'https://m.999.md/ru/list/transport/hydraulic-and-mechanical-equipment', 'https://m.999.md/ru/list/transport/service-station-furniture', 'https://m.999.md/ru/list/transport/lubrication-tool', 'https://m.999.md/ru/list/transport/bodywork-equipment', 'https://m.999.md/ru/list/transport/additional-car-equipment', 'https://m.999.md/ru/list/transport/hydraulic-oils', 'https://m.999.md/ru/list/transport/gear-oils', 'https://m.999.md/ru/list/transport/antifreeze', 'https://m.999.md/ru/list/transport/brake-fluid', 'https://m.999.md/ru/list/transport/automotive-lubricants', 'https://m.999.md/ru/list/transport/motor-oil', 'https://m.999.md/ru/list/transport/washer-fluid', 'https://m.999.md/ru/list/transport/oil-additives', 'https://m.999.md/ru/list/transport/fuel-additives', 'https://m.999.md/ru/list/transport/gear-oil-additives', 'https://m.999.md/ru/list/transport/washes-and-cleaners', 'https://m.999.md/ru/list/transport/fuel-additives-and-dispersants', 'https://m.999.md/ru/list/transport/car-2', 'https://m.999.md/ru/list/transport/cargo', 'https://m.999.md/ru/list/services/store-delivery', 'https://m.999.md/ru/list/transport/order-car', 'https://m.999.md/ru/list/transport/passenger', 'https://m.999.md/ru/list/transport/motoservice', 'https://m.999.md/ru/list/transport/rent-a-car', 'https://m.999.md/ru/list/transport/car-wash-accessories', 'https://m.999.md/ru/list/transport/car-shampoo', 'https://m.999.md/ru/list/transport/car-cleaner', 'https://m.999.md/ru/list/transport/polishes', 'https://m.999.md/ru/list/transport/anti-corrosion-coatings', 'https://m.999.md/ru/list/transport/interior-cleaning', 'https://m.999.md/ru/list/transport/rim-protection', 'https://m.999.md/ru/list/transport/autocosmetics-for-glasses-and-optics', 'https://m.999.md/ru/list/transport/miscellaneous']
        },
        {
            "title": "Строительство", "id": "999_stroi", "links": ['https://m.999.md/ru/list/construction-and-repair/boilers', 'https://m.999.md/ru/list/construction-and-repair/floor-heating', 'https://m.999.md/ru/list/construction-and-repair/stoves', 'https://m.999.md/ru/list/construction-and-repair/heaters', 'https://m.999.md/ru/list/construction-and-repair/fireplaces', 'https://m.999.md/ru/list/construction-and-repair/chimneys', 'https://m.999.md/ru/list/construction-and-repair/heating-radiators', 'https://m.999.md/ru/list/construction-and-repair/fireplace-accessories', 'https://m.999.md/ru/list/construction-and-repair/metal', 'https://m.999.md/ru/list/construction-and-repair/wood', 'https://m.999.md/ru/list/construction-and-repair/glass', 'https://m.999.md/ru/list/construction-and-repair/articles-of-concrete', 'https://m.999.md/ru/list/construction-and-repair/saws', 'https://m.999.md/ru/list/construction-and-repair/machine-tool', 'https://m.999.md/ru/list/construction-and-repair/impact-drivers', 'https://m.999.md/ru/list/construction-and-repair/drills', 'https://m.999.md/ru/list/construction-and-repair/hammer-drill', 'https://m.999.md/ru/list/construction-and-repair/sanders', 'https://m.999.md/ru/list/construction-and-repair/routers', 'https://m.999.md/ru/list/construction-and-repair/welding-machine', 'https://m.999.md/ru/list/construction-and-repair/solar-panels', 'https://m.999.md/ru/list/construction-and-repair/concrete-vibrators', 'https://m.999.md/ru/list/construction-and-repair/other-power-tools', 'https://m.999.md/ru/list/construction-and-repair/wood-planers', 'https://m.999.md/ru/list/construction-and-repair/power-jigsaws', 'https://m.999.md/ru/list/construction-and-repair/impact-wrenches', 'https://m.999.md/ru/list/construction-and-repair/jack-hammer', 'https://m.999.md/ru/list/construction-and-repair/heat-guns', 'https://m.999.md/ru/list/construction-and-repair/industrial-vacuum-cleaners', 'https://m.999.md/ru/list/construction-and-repair/electric-screwdriver', 'https://m.999.md/ru/list/construction-and-repair/wall-chaser', 'https://m.999.md/ru/list/construction-and-repair/concrete-mixers', 'https://m.999.md/ru/list/construction-and-repair/soldering-iron', 'https://m.999.md/ru/list/construction-and-repair/nailers', 'https://m.999.md/ru/list/construction-and-repair/multitools', 'https://m.999.md/ru/list/construction-and-repair/power-shears', 'https://m.999.md/ru/list/construction-and-repair/glue-guns', 'https://m.999.md/ru/list/construction-and-repair/paint-sprayers', 'https://m.999.md/ru/list/construction-and-repair/tile-saws', 'https://m.999.md/ru/list/construction-and-repair/plastic-pipe-welding-machines', 'https://m.999.md/ru/list/construction-and-repair/consumables', 'https://m.999.md/ru/list/construction-and-repair/miscellaneous', 'https://m.999.md/ru/list/construction-and-repair/lumber', 'https://m.999.md/ru/list/construction-and-repair/finishing-and-facing-materials', 'https://m.999.md/ru/list/construction-and-repair/roofing-materials', 'https://m.999.md/ru/list/construction-and-repair/the-heat-and-sound-insulating-materials', 'https://m.999.md/ru/list/construction-and-repair/building-materials', 'https://m.999.md/ru/list/construction-and-repair/gas-powered', 'https://m.999.md/ru/list/construction-and-repair/pumps-and-pump', 'https://m.999.md/ru/list/construction-and-repair/hand-tool', 'https://m.999.md/ru/list/construction-and-repair/construction-equipment', 'https://m.999.md/ru/list/construction-and-repair/pneumatics', 'https://m.999.md/ru/list/construction-and-repair/lighting', 'https://m.999.md/ru/list/construction-and-repair/windows-doors', 'https://m.999.md/ru/list/household-appliances/air-conditioners', 'https://m.999.md/ru/list/construction-and-repair/repairs', 'https://m.999.md/ru/list/construction-and-repair/construction-work', 'https://m.999.md/ru/list/construction-and-repair/plumbing', 'https://m.999.md/ru/list/construction-and-repair/electrical-2', 'https://m.999.md/ru/list/construction-and-repair/design-and-architecture', 'https://m.999.md/ru/list/construction-and-repair/metal-2', 'https://m.999.md/ru/list/construction-and-repair/rental-equipment', 'https://m.999.md/ru/list/construction-and-repair/plumbing-bath', 'https://m.999.md/ru/list/construction-and-repair/pipes', 'https://m.999.md/ru/list/construction-and-repair/sinks', 'https://m.999.md/ru/list/construction-and-repair/taps', 'https://m.999.md/ru/list/construction-and-repair/towel-racks']
        },
        {
            "title": "Одежда", "id": "999_clothes", "links": ['https://m.999.md/ru/list/clothes-and-shoes/clothing-for-men', 'https://m.999.md/ru/list/clothes-and-shoes/shoes-for-men', 'https://m.999.md/ru/list/clothes-and-shoes/clothing-for-girls', 'https://m.999.md/ru/list/clothes-and-shoes/childrens-shoes', 'https://m.999.md/ru/list/clothes-and-shoes/sports-shoes', 'https://m.999.md/ru/list/clothes-and-shoes/sports-uniforms', 'https://m.999.md/ru/list/clothes-and-shoes/thermal-underwear', 'https://m.999.md/ru/list/clothes-and-shoes/miscellaneous', 'https://m.999.md/ru/list/clothes-and-shoes/special-clothing', 'https://m.999.md/ru/list/clothes-and-shoes/carnival-costumes', 'https://m.999.md/ru/list/clothes-and-shoes/wedding-clothes', 'https://m.999.md/ru/list/clothes-and-shoes/wedding-shoes', 'https://m.999.md/ru/list/clothes-and-shoes/wedding-accessories', 'https://m.999.md/ru/list/clothes-and-shoes/clothes-for-women', 'https://m.999.md/ru/list/clothes-and-shoes/shoes-for-women', 'https://m.999.md/ru/list/clothes-and-shoes/female-underwear', 'https://m.999.md/ru/list/clothes-and-shoes/bags-briefcases', 'https://m.999.md/ru/list/clothes-and-shoes/watches', 'https://m.999.md/ru/list/clothes-and-shoes/jewelry', 'https://m.999.md/ru/list/clothes-and-shoes/hats', 'https://m.999.md/ru/list/clothes-and-shoes/belts-gloves', 'https://m.999.md/ru/list/clothes-and-shoes/glasses', 'https://m.999.md/ru/list/clothes-and-shoes/neckties-shawls', 'https://m.999.md/ru/list/clothes-and-shoes/rent-clothes', 'https://m.999.md/ru/list/clothes-and-shoes/laundry', 'https://m.999.md/ru/list/clothes-and-shoes/delivery-clothes']
        },
        {
            "title": "Работа", "id": "999_work", "links": ['https://m.999.md/ru/list/work/abroad', 'https://m.999.md/ru/list/work/df', 'https://m.999.md/ru/list/work/lat', 'https://m.999.md/ru/list/work/auto-repair', 'https://m.999.md/ru/list/work/aef', 'https://m.999.md/ru/list/work/carwash', 'https://m.999.md/ru/list/work/courier', 'https://m.999.md/ru/list/work/cleaner', 'https://m.999.md/ru/list/work/dw', 'https://m.999.md/ru/list/work/nanny', 'https://m.999.md/ru/list/work/general-workers', 'https://m.999.md/ru/list/work/oms', 'https://m.999.md/ru/list/work/project-manager', 'https://m.999.md/ru/list/work/accounting', 'https://m.999.md/ru/list/work/auditing', 'https://m.999.md/ru/list/work/bcl', 'https://m.999.md/ru/list/work/pw', 'https://m.999.md/ru/list/work/et', 'https://m.999.md/ru/list/work/pm', 'https://m.999.md/ru/list/work/sc', 'https://m.999.md/ru/list/work/am', 'https://m.999.md/ru/list/work/sr', 'https://m.999.md/ru/list/work/sm', 'https://m.999.md/ru/list/work/sbt', 'https://m.999.md/ru/list/work/hr', 'https://m.999.md/ru/list/work/psj', 'https://m.999.md/ru/list/work/agroindustry', 'https://m.999.md/ru/list/work/zootechnics', 'https://m.999.md/ru/list/work/dg', 'https://m.999.md/ru/list/work/art', 'https://m.999.md/ru/list/work/entertainment', 'https://m.999.md/ru/list/work/fva', 'https://m.999.md/ru/list/work/massage', 'https://m.999.md/ru/list/work/medical-staff', 'https://m.999.md/ru/list/work/pharmaceutics', 'https://m.999.md/ru/list/work/development', 'https://m.999.md/ru/list/work/seo', 'https://m.999.md/ru/list/work/computer-master', 'https://m.999.md/ru/list/work/it-management', 'https://m.999.md/ru/list/work/telecommunications', 'https://m.999.md/ru/list/work/sa', 'https://m.999.md/ru/list/work/copywriting', 'https://m.999.md/ru/list/work/marketing', 'https://m.999.md/ru/list/work/promoter', 'https://m.999.md/ru/list/work/pr', 'https://m.999.md/ru/list/work/bs', 'https://m.999.md/ru/list/work/real-estate', 'https://m.999.md/ru/list/work/da', 'https://m.999.md/ru/list/work/pbm', 'https://m.999.md/ru/list/work/jurisprudence', 'https://m.999.md/ru/list/work/insurance', 'https://m.999.md/ru/list/work/presenter', 'https://m.999.md/ru/list/work/translator', 'https://m.999.md/ru/list/work/journalism', 'https://m.999.md/ru/list/work/producer', 'https://m.999.md/ru/list/work/schooling', 'https://m.999.md/ru/list/work/educator', 'https://m.999.md/ru/list/work/foreign-languages', 'https://m.999.md/ru/list/work/gb', 'https://m.999.md/ru/list/work/ss', 'https://m.999.md/ru/list/work/tourism', 'https://m.999.md/ru/list/work/cuisine-workers', 'https://m.999.md/ru/list/work/waiter-bartender', 'https://m.999.md/ru/list/work/administration-of-restaurant', 'https://m.999.md/ru/list/work/other', 'https://m.999.md/ru/list/work/muab', 'https://m.999.md/ru/list/work/administrator-salon', 'https://m.999.md/ru/list/work/mp', 'https://m.999.md/ru/list/work/hs', 'https://m.999.md/ru/list/work/coach']
        },
        {
            "title": "Сель.хоз", "id": "999_agriculture", "links": ['https://m.999.md/ru/list/agriculture/other', 'https://m.999.md/ru/list/agriculture/agricultural-machinery', 'https://m.999.md/ru/list/agriculture/livestock', 'https://m.999.md/ru/list/agriculture/aviculture', 'https://m.999.md/ru/list/agriculture/animal-feed', 'https://m.999.md/ru/list/agriculture/beekeeping-and-honey', 'https://m.999.md/ru/list/agriculture/pisciculture', 'https://m.999.md/ru/list/agriculture/fertilizers-and-chemicals', 'https://m.999.md/ru/list/agriculture/seeds-and-seedlings', 'https://m.999.md/ru/list/agriculture/farm-equipment', 'https://m.999.md/ru/list/construction-and-repair/gas-powered', 'https://m.999.md/ru/list/agriculture/wood-coal-fuel', 'https://m.999.md/ru/list/agriculture/tools', 'https://m.999.md/ru/list/agriculture/grain-cereals-flours', 'https://m.999.md/ru/list/agriculture/vegetables-and-fruits', 'https://m.999.md/ru/list/agriculture/nuts', 'https://m.999.md/ru/list/agriculture/meat-bird-fish', 'https://m.999.md/ru/list/agriculture/oil', 'https://m.999.md/ru/list/agriculture/berries-mushrooms', 'https://m.999.md/ru/list/all-for-celebrations/elite-alcohol', 'https://m.999.md/ru/list/agriculture/dairy-products', 'https://m.999.md/ru/list/agriculture/dried-fruits', 'https://m.999.md/ru/list/agriculture/services']
        },
        {
            "title": "Услуги", "id": "999_services", "links": ['https://m.999.md/ru/list/transport/cargo', 'https://m.999.md/ru/list/transport/car-2', 'https://m.999.md/ru/list/transport/passenger', 'https://m.999.md/ru/list/all-for-celebrations/transport-for-celebrations', 'https://m.999.md/ru/list/transport/rent-a-car', 'https://m.999.md/ru/list/services/store-delivery', 'https://m.999.md/ru/list/construction-and-repair/repairs', 'https://m.999.md/ru/list/construction-and-repair/electrical-2', 'https://m.999.md/ru/list/construction-and-repair/plumbing', 'https://m.999.md/ru/list/construction-and-repair/construction-work', 'https://m.999.md/ru/list/construction-and-repair/metal-2', 'https://m.999.md/ru/list/construction-and-repair/construction-equipment', 'https://m.999.md/ru/list/construction-and-repair/design-and-architecture', 'https://m.999.md/ru/list/household-appliances/appliance-repair', 'https://m.999.md/ru/list/all-for-home-and-office/cleaning-services', 'https://m.999.md/ru/list/clothes-and-shoes/laundry', 'https://m.999.md/ru/list/audio-video-photo/repair', 'https://m.999.md/ru/list/furniture-and-interior/custom-furniture', 'https://m.999.md/ru/list/all-else/funeral-services', 'https://m.999.md/ru/list/clothes-and-shoes/delivery-clothes', 'https://m.999.md/ru/list/phone-and-communication/service-and-repair-of-telephones', 'https://m.999.md/ru/list/real-estate/services', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/massage', 'https://m.999.md/ru/list/sports-health-and-beauty/hair-care', 'https://m.999.md/ru/list/sports-health-and-beauty/beauty-and-makeup', 'https://m.999.md/ru/list/sports-health-and-beauty/nails-manicure-pedicure', 'https://m.999.md/ru/list/services/courses-and-trainings', 'https://m.999.md/ru/list/work/schooling', 'https://m.999.md/ru/list/work/foreign-languages', 'https://m.999.md/ru/list/children-world/education-and-child-care', 'https://m.999.md/ru/list/work/educator', 'https://m.999.md/ru/list/all-else/reports-and-dissertations', 'https://m.999.md/ru/list/agriculture/services', 'https://m.999.md/ru/list/business/legal-services', 'https://m.999.md/ru/list/business/accounting-and-audit-services', 'https://m.999.md/ru/list/all-else/security-and-safety', 'https://m.999.md/ru/list/business/leasing', 'https://m.999.md/ru/list/business/doing-business', 'https://m.999.md/ru/list/business/insurance-services-and-consulting', 'https://m.999.md/ru/list/all-for-celebrations/photo-video-services', 'https://m.999.md/ru/list/all-for-celebrations/cookery', 'https://m.999.md/ru/list/all-for-celebrations/musicians', 'https://m.999.md/ru/list/all-for-celebrations/maintenance-of-celebrations', 'https://m.999.md/ru/list/business/dev-support-sites', 'https://m.999.md/ru/list/computers-and-office-equipment/computer-services', 'https://m.999.md/ru/list/animals-and-plants/tying', 'https://m.999.md/ru/list/animals-and-plants/care', 'https://m.999.md/ru/list/animals-and-plants/missing', 'https://m.999.md/ru/list/business/printing-design', 'https://m.999.md/ru/list/business/advertising-services-and-development', 'https://m.999.md/ru/list/services/other']
        },
        {
            "title": "Животные", "id": "999_animals", "links": ['https://m.999.md/ru/list/animals-and-plants/dogs', 'https://m.999.md/ru/list/animals-and-plants/cats', 'https://m.999.md/ru/list/animals-and-plants/the-birds', 'https://m.999.md/ru/list/animals-and-plants/fish', 'https://m.999.md/ru/list/animals-and-plants/other-animals', 'https://m.999.md/ru/list/animals-and-plants/accessories-for-animals', 'https://m.999.md/ru/list/animals-and-plants/missing', 'https://m.999.md/ru/list/animals-and-plants/plants-and-flowers', 'https://m.999.md/ru/list/animals-and-plants/inventory', 'https://m.999.md/ru/list/animals-and-plants/miscellaneous', 'https://m.999.md/ru/list/animals-and-plants/tying', 'https://m.999.md/ru/list/animals-and-plants/care']
        },
        {
            "title": "Спорт", "id": "999_sport", "links": ['https://m.999.md/ru/list/sports-health-and-beauty/trainers-and-equipment', 'https://m.999.md/ru/list/sports-health-and-beauty/nutrition', 'https://m.999.md/ru/list/sports-health-and-beauty/pools', 'https://m.999.md/ru/list/sports-health-and-beauty/sports-clubs', 'https://m.999.md/ru/list/sports-health-and-beauty/scooters-skates-skis', 'https://m.999.md/ru/list/sports-health-and-beauty/perfumes-cosmetics', 'https://m.999.md/ru/list/sports-health-and-beauty/care', 'https://m.999.md/ru/list/sports-health-and-beauty/medical-facilities', 'https://m.999.md/ru/list/sports-health-and-beauty/drugs-and-medicines', 'https://m.999.md/ru/list/sports-health-and-beauty/essential-oils-teas-herbs', 'https://m.999.md/ru/list/sports-health-and-beauty/miscellaneous', 'https://m.999.md/ru/list/transport/bicycles', 'https://m.999.md/ru/list/transport/spare-parts-for-bicycles', 'https://m.999.md/ru/list/clothes-and-shoes/sports-shoes', 'https://m.999.md/ru/list/clothes-and-shoes/glasses', 'https://m.999.md/ru/list/clothes-and-shoes/thermal-underwear', 'https://m.999.md/ru/list/clothes-and-shoes/sports-uniforms', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/massage', 'https://m.999.md/ru/list/sports-health-and-beauty/traditional-medicine', 'https://m.999.md/ru/list/sports-health-and-beauty/hair-care', 'https://m.999.md/ru/list/sports-health-and-beauty/beauty-and-makeup', 'https://m.999.md/ru/list/sports-health-and-beauty/nails-manicure-pedicure']
        },
        {
            "title": "Туризм", "id": "999_tourism", "links": ['https://m.999.md/ru/list/tourism-leisure-and-entertainment/holidays-abroad', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/rest-in-moldova', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/massage', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/entertainment-and-recreation', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/sauna', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/tents', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/leisure-products', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/flashlights', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/backpacks-and-bags', 'https://m.999.md/ru/list/audio-video-photo/binoculars-telescopes-microscopes', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/guns-and-knives', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/fishing-rods-and-tackles', 'https://m.999.md/ru/list/clothes-and-shoes/special-clothing', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/miscellaneous']
        },
        {
            "title": "Бизнес", "id": "999_busines", "links": ['https://m.999.md/ru/list/business/leasing', 'https://m.999.md/ru/list/business/legal-services', 'https://m.999.md/ru/list/business/advertising-services-and-development', 'https://m.999.md/ru/list/business/dev-support-sites', 'https://m.999.md/ru/list/business/printing-design', 'https://m.999.md/ru/list/business/accounting-and-audit-services', 'https://m.999.md/ru/list/business/insurance-services-and-consulting', 'https://m.999.md/ru/list/business/miscellaneous', 'https://m.999.md/ru/list/all-else/professional-equipment', 'https://m.999.md/ru/list/business/cash-registers-and-scales', 'https://m.999.md/ru/list/business/the-current-business', 'https://m.999.md/ru/list/business/doing-business', 'https://m.999.md/ru/list/business/shares-in', 'https://m.999.md/ru/list/business/tenders-and-auctions']
        },
        {
            "title": "Инструменты", "id": "999_instruments", "links": ['https://m.999.md/ru/list/musical-instruments/audio-mixers', 'https://m.999.md/ru/list/musical-instruments/amplifiers', 'https://m.999.md/ru/list/audio-video-photo/acoustics-columns', 'https://m.999.md/ru/list/audio-video-photo/microphones', 'https://m.999.md/ru/list/musical-instruments/dj-equipment', 'https://m.999.md/ru/list/musical-instruments/stage-equipment', 'https://m.999.md/ru/list/musical-instruments/guitars', 'https://m.999.md/ru/list/musical-instruments/effects', 'https://m.999.md/ru/list/musical-instruments/keyboard-instruments', 'https://m.999.md/ru/list/musical-instruments/accordions', 'https://m.999.md/ru/list/musical-instruments/strings', 'https://m.999.md/ru/list/musical-instruments/winds', 'https://m.999.md/ru/list/musical-instruments/percussion', 'https://m.999.md/ru/list/musical-instruments/learning', 'https://m.999.md/ru/list/musical-instruments/repair', 'https://m.999.md/ru/list/musical-instruments/recording-and-mixing', 'https://m.999.md/ru/list/musical-instruments/rent', 'https://m.999.md/ru/list/musical-instruments/accessories-and-components', 'https://m.999.md/ru/list/musical-instruments/racks-frames-chairs', 'https://m.999.md/ru/list/musical-instruments/cases', 'https://m.999.md/ru/list/musical-instruments/miscellaneous']
        },
        {
            "title": "Уход за домом", "id": "999_house_h", "links": ['https://m.999.md/ru/list/household-appliances/hair-dryers', 'https://m.999.md/ru/list/household-appliances/hair-styling-tools', 'https://m.999.md/ru/list/household-appliances/hair-clippers', 'https://m.999.md/ru/list/household-appliances/trimmers', 'https://m.999.md/ru/list/household-appliances/electric-shavers', 'https://m.999.md/ru/list/household-appliances/epilators', 'https://m.999.md/ru/list/household-appliances/scales', 'https://m.999.md/ru/list/household-appliances/massagers', 'https://m.999.md/ru/list/household-appliances/manicure-pedicure-kits', 'https://m.999.md/ru/list/household-appliances/electric-toothbrushes', 'https://m.999.md/ru/list/household-appliances/cosmetic-devices', 'https://m.999.md/ru/list/household-appliances/steam-cleaners', 'https://m.999.md/ru/list/household-appliances/vacuum-cleaners', 'https://m.999.md/ru/list/household-appliances/robot-vacuum-cleaners', 'https://m.999.md/ru/list/household-appliances/clothes-iron', 'https://m.999.md/ru/list/household-appliances/knitting-machines', 'https://m.999.md/ru/list/household-appliances/sewing-machines', 'https://m.999.md/ru/list/household-appliances/accessories-for-sewing', 'https://m.999.md/ru/list/household-appliances/shoe-dryer', 'https://m.999.md/ru/list/household-appliances/heating-pad', 'https://m.999.md/ru/list/household-appliances/clothes-cleaning-accessories', 'https://m.999.md/ru/list/audio-video-photo/tv', 'https://m.999.md/ru/list/household-appliances/air-conditioners', 'https://m.999.md/ru/list/household-appliances/boilers', 'https://m.999.md/ru/list/household-appliances/gas-boilers', 'https://m.999.md/ru/list/household-appliances/air-cleaners-and-humidifiers', 'https://m.999.md/ru/list/household-appliances/miscellaneous', 'https://m.999.md/ru/list/household-appliances/washing-machines', 'https://m.999.md/ru/list/household-appliances/refrigerators', 'https://m.999.md/ru/list/household-appliances/stove-oven', 'https://m.999.md/ru/list/household-appliances/microwaves', 'https://m.999.md/ru/list/household-appliances/dishwashers', 'https://m.999.md/ru/list/household-appliances/hoods', 'https://m.999.md/ru/list/household-appliances/coffee-machines', 'https://m.999.md/ru/list/household-appliances/meat-grinders', 'https://m.999.md/ru/list/household-appliances/juicers', 'https://m.999.md/ru/list/household-appliances/multicookers', 'https://m.999.md/ru/list/household-appliances/kettles', 'https://m.999.md/ru/list/household-appliances/thermometers', 'https://m.999.md/ru/list/household-appliances/blenders', 'https://m.999.md/ru/list/household-appliances/bread-machines', 'https://m.999.md/ru/list/household-appliances/electric-stoves', 'https://m.999.md/ru/list/household-appliances/portable-stovetops', 'https://m.999.md/ru/list/household-appliances/toasters', 'https://m.999.md/ru/list/household-appliances/kitchen-machine', 'https://m.999.md/ru/list/household-appliances/mixers', 'https://m.999.md/ru/list/household-appliances/steam-cookers', 'https://m.999.md/ru/list/household-appliances/electro-grills', 'https://m.999.md/ru/list/household-appliances/water-filters-and-coolers', 'https://m.999.md/ru/list/household-appliances/sandwich-makers-waffle-makers', 'https://m.999.md/ru/list/household-appliances/fryers', 'https://m.999.md/ru/list/household-appliances/coffee-grinders', 'https://m.999.md/ru/list/household-appliances/slicer-machines', 'https://m.999.md/ru/list/household-appliances/kitchen-scales', 'https://m.999.md/ru/list/household-appliances/pasta-machines', 'https://m.999.md/ru/list/household-appliances/yogurt-makers', 'https://m.999.md/ru/list/household-appliances/egg-cookers', 'https://m.999.md/ru/list/household-appliances/milk-frothers', 'https://m.999.md/ru/list/household-appliances/fruit-dryers', 'https://m.999.md/ru/list/household-appliances/pancake-makers', 'https://m.999.md/ru/list/household-appliances/ice-cream-machines', 'https://m.999.md/ru/list/household-appliances/nitratometers', 'https://m.999.md/ru/list/household-appliances/appliance-repair']
        },
        {
            "title": "Подарки", "id": "999_gifts", "links": ['https://m.999.md/ru/list/all-for-celebrations/little-touches', 'https://m.999.md/ru/list/all-for-celebrations/gifts-for-fans-of-smoking', 'https://m.999.md/ru/list/all-for-celebrations/flowers', 'https://m.999.md/ru/list/tourism-leisure-and-entertainment/guns-and-knives', 'https://m.999.md/ru/list/furniture-and-interior/antiques', 'https://m.999.md/ru/list/all-for-celebrations/elite-alcohol', 'https://m.999.md/ru/list/all-for-celebrations/fireworks-sky-lanterns', 'https://m.999.md/ru/list/all-for-celebrations/miscellaneous', 'https://m.999.md/ru/list/all-for-celebrations/cookery', 'https://m.999.md/ru/list/all-for-celebrations/photo-video-services', 'https://m.999.md/ru/list/all-for-celebrations/musicians', 'https://m.999.md/ru/list/all-for-celebrations/maintenance-of-celebrations', 'https://m.999.md/ru/list/business/printing-design', 'https://m.999.md/ru/list/all-for-celebrations/transport-for-celebrations']
        },
        {
            "title": "Детский мир", "id": "999_kid_world", "links": ['https://m.999.md/ru/list/clothes-and-shoes/childrens-shoes', 'https://m.999.md/ru/list/clothes-and-shoes/clothing-for-girls', 'https://m.999.md/ru/list/clothes-and-shoes/carnival-costumes', 'https://m.999.md/ru/list/children-world/stroller', 'https://m.999.md/ru/list/children-world/toys', 'https://m.999.md/ru/list/children-world/miscellaneous', 'https://m.999.md/ru/list/children-world/furniture-for-children', 'https://m.999.md/ru/list/children-world/car', 'https://m.999.md/ru/list/children-world/power-and-accessories-for-food', 'https://m.999.md/ru/list/children-world/walkers-slings-and-cots', 'https://m.999.md/ru/list/sports-health-and-beauty/scooters-skates-skis', 'https://m.999.md/ru/list/transport/electric-scooters', 'https://m.999.md/ru/list/children-world/care-and-hygiene', 'https://m.999.md/ru/list/children-world/education-and-child-care']
        },
        {
            "title": "Встречи", "id": "999_dates", "links": ['https://m.999.md/ru/list/dating-and-greetings/i-need-a-man', 'https://m.999.md/ru/list/dating-and-greetings/looking-for-a-woman', 'https://m.999.md/ru/list/dating-and-greetings/looking-for-friends', 'https://m.999.md/ru/list/dating-and-greetings/the-couple-met', 'https://m.999.md/ru/list/dating-and-greetings/miscellaneous', 'https://m.999.md/ru/list/dating-and-greetings/marriage-agencies']
        },
    ]

    def get_link_by_id(self, id: str):
        for i in self.categories:
            if id == i.get('id'):
                return i.get('links')

    def get_categories_for_markup(self):
        return [
            {"text": x.get('title'), "callback_data": x.get('id')}
            for x in self.categories
        ]

    def check_category_id(self, id: str):
        for i in self.categories:
            if id == i.get('id'):
                return True
        return False

    def check_link(self, link: str):
        return link.startswith('https://m.999.md/ru/list')

    def parse(self, links: list, limit: int, chat_id: int) -> bool:
        Thread(target=self.__parse, args=(links, limit, chat_id)).start()
        return True
    
    def remove_duplicates_by_phone(self, items: list) -> list:
        a = list()
        b = list()
        for i in items:
            if i[1] not in b:
                a.append(i)
                b.append(i[1])
        return a

    
    def __parse(self, links: list, limit: int, chat_id: int):
        contacts = list()
        for link in links:
            try:
                base_link = link
                page = 1

                link = lambda: base_link + f'&page={page}' if '?' in base_link else base_link + f'?page={page}'
                resp = requests.get(link())
                if resp.status_code // 100 != 2:
                    return
                soup = bs4.BeautifulSoup(resp.text, 'lxml')        


                while len(contacts) < limit or limit == -1:
                    elements = soup.find('ul', {'class': 'block-items is-photo-view'})
                    if elements is None:
                        break

                    elements = elements.find_all('li', {'class': 'block-items__item'})
                    if elements is None:
                        break

                    for element in elements:
                        if len(contacts) > limit and limit != -1:
                            break
                        try:
                            current_link = 'https://m.999.md' + element.find('a', {'class': 'block-items__item__link js-item-ad'})['href']
                            
                            info = self.__parse_current_page(current_link)
                            print(info)
                            contacts.append(info)
                        except:
                            pass
                        finally:
                            time.sleep(1)
                        
                        contacts = self.remove_duplicates_by_phone(contacts)
                    print(len(contacts))
                    if len(contacts) > limit and limit != -1:
                        break
                    
                    try:
                        is_next = soup.find('a', {'class': 'block-nav__next'})['href']
                        if is_next is None:
                            break
                    except:
                        break

                    page += 1
                    resp = requests.get(link())
                    if resp.status_code // 100 != 2:
                        break
                    soup = bs4.BeautifulSoup(resp.text, 'lxml') 
            except Exception as e:
                print(e)  
        
        filename = uuid4().hex + '.xlsx'
        filename = f"{base_link.split('/')[-1]}_{limit}_{filename}"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        contacts = [('Имя', 'Номер телефона')] + contacts
        
        row = 0
        col = 0

        for item, cost in contacts:
            worksheet.write(row, col, item)
            worksheet.write(row, col+1, cost)
            row += 1

        workbook.close()

        f = open(filename, 'rb')

        self.bot.send_document(chat_id, f)
        os.remove(filename)

    def __parse_current_page(self, link: str):
        resp = requests.get(link)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'lxml')

        contacts = soup.find('div', {'class': 'item-page__author-info'})

        name = contacts.find('a', {'class': 'item-page__author-info__item_user'}).text.strip()
        phone = contacts.find('a', {'class': 'item-page__author-info__item_phone'})['href'].split(':')[-1].strip()
        
        while '  ' in name:
            name = name.replace('  ', ' ')
        return (name, phone)

