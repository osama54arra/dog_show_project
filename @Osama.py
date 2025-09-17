#!/usr/bin/env python3
# PROGRAMMER: [Osama Abuarra]
# DATE CREATED: [ Sep 15th 2025]
# REVISED DATE: 
# PURPOSE: Project - Image Classification for City Dog Show

from time import time, sleep
import argparse
import os
from classifier import classifier as classify_image

# ------------------------------------------------------------
# TODO 1: Define get_i/nput_args function
# ------------------------------------------------------------
def get_input_args():
    """
    Retrieves and parses the 3 command line arguments provided by the user.
    """
    parser = argparse.ArgumentParser(description="Classify pet images using CNN models.")
    parser.add_argument('--dir', type=str, default='pet_images/',
                        help='مسار المجلد الذي يحتوي على صور الحيوانات الأليفة')
    parser.add_argument('--arch', type=str, default='vgg',
                        choices=['resnet', 'alexnet', 'vgg'],
                        help='اسم بنية نموذج CNN للاستخدام: resnet, alexnet, أو vgg')
    parser.add_argument('--dogfile', type=str, default='dognames.txt',
                        help='مسار الملف الذي يحتوي على قائمة بأسماء السلالات المعترف بها')
    return parser.parse_args()

# ------------------------------------------------------------
# TODO 2: Define get_pet_labels function
# ------------------------------------------------------------
def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based on the filenames.
    """
    results_dic = {}
    filenames = os.listdir(image_dir)
    
    for fname in filenames:
        if fname.startswith('.'):  # تجاهل الملفات المخفية
            continue
        # تحويل Beagle_01141.jpg → beagle
        pet_label = " ".join(fname.split('_')[:-1]).lower().strip()
        if fname not in results_dic:
            results_dic[fname] = [pet_label]
        else:
            print(f"** تحذير: ملف مكرر: {fname}")
    return results_dic

# ------------------------------------------------------------
# TODO 3: Define classify_images function
# ------------------------------------------------------------
def classify_images(images_dir, results_dic, model):
    """
    Classifies images and compares labels.
    """
    for filename in results_dic:
        img_path = os.path.join(images_dir, filename)
        classifier_label = classify_image(img_path, model)
        classifier_label = classifier_label.lower().strip()
        pet_label = results_dic[filename][0]
        is_match = 1 if classifier_label == pet_label else 0
        results_dic[filename].extend([classifier_label, is_match])

# ------------------------------------------------------------
# TODO 4: Define adjust_results4_isadog function
# ------------------------------------------------------------
def adjust_results4_isadog(results_dic, dogfile):
    """
    Adjusts results to indicate whether labels are dogs.
    """
    dognames_set = set()
    with open(dogfile, 'r') as f:
        for line in f:
            dognames_set.add(line.strip().lower())
    
    for filename in results_dic:
        pet_label = results_dic[filename][0]
        classifier_label = results_dic[filename][1]
        
        is_pet_dog = 1 if pet_label in dognames_set else 0
        
        is_classifier_dog = 0
        for name in classifier_label.split(','):
            if name.strip() in dognames_set:
                is_classifier_dog = 1
                break
                
        results_dic[filename].extend([is_pet_dog, is_classifier_dog])

# ------------------------------------------------------------
# TODO 5: Define calculates_results_stats function
# ------------------------------------------------------------
def calculates_results_stats(results_dic):
    """
    Calculates statistics of results.
    """
    stats = {
        'n_images': len(results_dic),
        'n_dogs_img': 0,
        'n_notdogs_img': 0,
        'n_match': 0,
        'n_correct_dogs': 0,
        'n_correct_notdogs': 0,
        'n_correct_breed': 0
    }
    
    for key in results_dic:
        pet_label, classifier_label, is_match, is_pet_dog, is_classifier_dog = results_dic[key]
        stats['n_match'] += is_match
        if is_pet_dog:
            stats['n_dogs_img'] += 1
            if is_classifier_dog:
                stats['n_correct_dogs'] += 1
            if is_match:
                stats['n_correct_breed'] += 1
        else:
            stats['n_notdogs_img'] += 1
            if not is_classifier_dog:
                stats['n_correct_notdogs'] += 1
                
    # حساب النسب المئوية
    stats['pct_match'] = (stats['n_match'] / stats['n_images']) * 100 if stats['n_images'] > 0 else 0
    stats['pct_correct_dogs'] = (stats['n_correct_dogs'] / stats['n_dogs_img']) * 100 if stats['n_dogs_img'] > 0 else 0
    stats['pct_correct_breed'] = (stats['n_correct_breed'] / stats['n_dogs_img']) * 100 if stats['n_dogs_img'] > 0 else 0
    stats['pct_correct_notdogs'] = (stats['n_correct_notdogs'] / stats['n_notdogs_img']) * 100 if stats['n_notdogs_img'] > 0 else 0
    
    return stats

# ------------------------------------------------------------
# TODO 6: Define print_results function
# ------------------------------------------------------------
def print_results(results_dic, results_stats, model_name):
    """
    Prints summary results.
    """
    print(f"\n\n*** نتائج ملخصة لنموذج CNN: {model_name.upper()} ***")
    print(f"عدد الصور: {results_stats['n_images']}")
    print(f"عدد صور الكلاب: {results_stats['n_dogs_img']}")
    print(f"عدد صور غير الكلاب: {results_stats['n_notdogs_img']}")
    print(f"% التصنيف الصحيح للكلاب: {results_stats['pct_correct_dogs']:.1f}%")
    print(f"% التصنيف الصحيح للسلالة: {results_stats['pct_correct_breed']:.1f}%")
    print(f"% التصنيف الصحيح لغير الكلاب: {results_stats['pct_correct_notdogs']:.1f}%")

# ------------------------------------------------------------
# Main Function
# ------------------------------------------------------------
def main():
    # TODO 0: قياس الوقت
    start_time = time()

    # TODO 1: قراءة الوسيطات
    in_arg = get_input_args()
    print("الوسيطات:")
    print(f"  --dir: {in_arg.dir}")
    print(f"  --arch: {in_arg.arch}")
    print(f"  --dogfile: {in_arg.dogfile}")

    # TODO 2: إنشاء تسميات الصور
    results_dic = get_pet_labels(in_arg.dir)
    print(f"\nعدد الصور: {len(results_dic)}")

    # TODO 3: تصنيف الصور
    classify_images(in_arg.dir, results_dic, in_arg.arch)

    # TODO 4: تصنيف كـ كلب/ليس كلب
    adjust_results4_isadog(results_dic, in_arg.dogfile)

    # TODO 5: حساب الإحصائيات
    results_stats = calculates_results_stats(results_dic)

    # TODO 6: طباعة النتائج
    print_results(results_dic, results_stats, in_arg.arch)

    # TODO 0: إنهاء قياس الوقت
    end_time = time()
    tot_time = end_time - start_time
    print(f"\n** الوقت الإجمالي المنقضي: {int(tot_time//3600)}:{int((tot_time%3600)//60)}:{int(tot_time%60)}")

# ------------------------------------------------------------
# Run Main
# ------------------------------------------------------------
if __name__ == "__main__":
    main()