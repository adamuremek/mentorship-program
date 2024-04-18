"""
/*********************************************************************/
/* FILE NAME: filters.py                                    */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Adam U. & Jordan A.                                   */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* The project enhances the functionality of the Django web platform */
/* by providing custom template filters that can be used across      */
/* various templates to manipulate and display data more efficiently.*/
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file includes custom Django template filters which are       */
/* reusable components within the templating engine. This specific   */
/* filter 'get_value' allows for dynamic data retrieval from         */
/* dictionaries within templates, improving the flexibility and      */
/* cleanliness of template code.                                     */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - template: Module for Django templating features                 */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

from django.template.defaulttags import register 

@register.filter
def get_value(dictionary: dict, key):
    """
    Authors Adam U. & Jordan A.

    Used to retrieve the dictionary value using a key within the html template.
    
    This was put here for the time being, sorry for the crappy definition location!
    """
    return dictionary.get(key)
