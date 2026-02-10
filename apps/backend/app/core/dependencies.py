from fastapi import Depends, HTTPException, Header
from app.core.supabase import supabase

def get_current_user(authorization: str = Header(...)):
    """取得當前使用者"""
    try:
        token = authorization.replace("Bearer ", "")
        user = supabase.auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="無效的 token")
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="無效的 token")

def get_current_org(
    user = Depends(get_current_user),
    org_id: str = Header(None, alias="X-Org-ID")
):
    """取得當前組織 (MVP 簡化版：若無組織表則使用個人 ID)"""
    if org_id:
        return org_id
        
    try:
        # 嘗試取得使用者的第一個 org
        result = supabase.table("org_members")\
            .select("org_id")\
            .eq("user_id", user.id)\
            .limit(1)\
            .execute()
        
        if result.data:
            return result.data[0]["org_id"]
    except Exception as e:
        # 如果表不存在或發生錯誤，暫時回退到使用 user.id 作為 org_id
        # 這能確保即使 Supabase 表還沒建好，基礎功能也能運作
        print(f"Organization lookup failed, falling back to user ID: {str(e)}")
        return str(user.id)
    
    # 如果真的沒資料，回傳 user.id 作為預設組織
    return str(user.id)
